# coding: utf-8
"""
Formex4 Builder
===============

This module can construct a Formex4 table from
an instance of type :class:`~benker.table.Table`.

:abbr:`Formex (Formalized Exchange of Electronic Publications)` describes the format for the exchange
of data between the Publication Office and its contractors. In particular, it defines the logical
markup for documents which are published in the different series of the Official Journal
of the European Union.

This builder allow you to convert Word document tables
into Formex4 tables using the Formex4 schema (formex-05.59-20170418.xd).

Specifications and examples:

- The Formex4 documentation and schema is available online in the Publication Office:
  `Formex Version 4 <http://formex.publications.europa.eu/formex-4/formex-4.htm>`_.

- An example of Formex4 table is available in the Schema documentation:
  `TBL <http://formex.publications.europa.eu/formex-4/manual/manual.htm#TBL>`_

"""
import collections
import re

from lxml import etree

from benker.builders.base_builder import BaseBuilder
from benker.builders.cals import get_colsep_attr
from benker.builders.cals import get_frame_attr
from benker.builders.cals import get_rowsep_attr
from benker.parsers.lxml_iterwalk import iterwalk
from benker.units import convert_value

CALS_NS = "https://lib.benker.com/schemas/cals.xsd"
CALS_PREFIX = "cals"

text_type = type(u"")


def revision_mark(name, attrs):
    target = etree.tounicode(etree.Element(name, attrib=attrs))
    target = target.replace("<{0} ".format(name), "").replace("/>", "")
    rev_pi = etree.ProcessingInstruction(name, target)
    return rev_pi


class Formex4Builder(BaseBuilder):
    """
    Formex4 builder used to convert tables into ``TBL`` elements
    according to the `TBL Schema <http://formex.publications.europa.eu/formex-4/manual/manual.htm#TBL>`_
    """

    # fmt: off
    def __init__(
        self,
        use_cals=False,
        cals_ns=CALS_NS,
        cals_prefix=CALS_PREFIX,
        width_unit="mm",
        **options
    ):
        # fmt: on
        """
        Initialize the builder.

        :param bool use_cals:
            Generate additional CALS-like elements and attributes
            to simplify the layout of Formex document in typesetting systems.

        :param str cals_ns:
            Namespace to use for CALS-like elements and attributes (requires: ``use_cals``).
            Set "" (empty) if you don't want to use namespace.

        :param str cals_prefix:
            Namespace prefix to use for CALS-like elements and attributes (requires: ``use_cals``).

        :param str width_unit:
            Unit to use for column widths (requires: ``use_cals``).
            Possible values are: 'cm', 'dm', 'ft', 'in', 'm', 'mm', 'pc', 'pt', 'px'.

        :keyword options: Extra conversion options.
            See :meth:`~benker.converters.base_converter.BaseConverter.convert_file`
            to have a list of all possible options.
        """
        # Internal state of the table used during building
        self._table = None
        self._table_colsep = u"0"  # for cals
        self._table_rowsep = u"0"  # for cals

        # NO.SEQ counter
        self._no_seq = 0

        # options
        self.use_cals = use_cals
        self.cals_ns = cals_ns
        self.cals_prefix = cals_prefix
        self.width_unit = width_unit

        super(Formex4Builder, self).__init__(**options)

    @property
    def ns_map(self):
        if self.use_cals and self.cals_ns:
            return {self.cals_prefix: self.cals_ns}
        return {}

    def get_cals_qname(self, name):
        if self.cals_ns:
            return etree.QName(self.cals_ns, name)
        return name

    def generate_table_tree(self, table):
        """
        Build the XML table from the Table instance.

        :type  table: benker.table.Table
        :param table: Table

        :return: Table tree
        """
        table_elem = self.build_tbl(table)
        return table_elem

    def build_tbl(self, table):
        """
        Build the Formex4 ``<TBL>`` element.

        Formex4 attributes:

        -   ``@NO.SEQ`` This mandatory attribute provides a sequence number to the table.
            This number represents the order in which the table appears in the document.

        -   ``@CLASS`` The CLASS attribute is mandatory and is used to specify the type of data
            contained in the table. The allowed values are:

            *   GEN: if the table contains general data (default value),
            *   SCHEDULE: if it is a schedule,
            *   RECAP: if it is a synoptic table.

            These two last values are only used for documents related to the general budget.

        -   ``@COLS`` This mandatory attribute provides the actual number of columns of the table.

        -   ``@PAGE.SIZE`` The PAGE.SIZE attribute takes one of these values:

            *   DOUBLE.LANDSCAPE: table on two A4 pages forming an A3 landscape page,
            *   DOUBLE.PORTRAIT: table on two A4 pages forming an A3 portrait page,
            *   SINGLE.LANDSCAPE: table on a single A4 page in landscape,
            *   SINGLE.PORTRAIT: table on a single A4 page in portrait (default).

        :type  table: benker.table.Table
        :param table: Table

        :return: The newly-created ``<TBL>`` element.

        .. versionchanged:: 0.5.0
           Add support for CALS-like elements and attributes.
           Add support for ``bgcolor`` (Table background color).
        """
        self._table = table
        table_styles = table.styles
        self._no_seq += 1
        attrs = {
            'NO.SEQ': u"{:04d}".format(self._no_seq),
            # 'CLASS': u"GEN",  # default value
            'COLS': str(len(table.cols)),
            # 'PAGE.SIZE': u"SINGLE.PORTRAIT",  # default value
        }
        if 'x-sect-orient' in table_styles:
            # size = (width x height) in 'pt'
            size = table_styles.get('x-sect-size', (595, 842))
            # C4 format 22.9cm x 32.4cm is a little bigger than A4
            if (size[0] <= 649 and size[1] <= 918) or (size[0] <= 918 and size[1] <= 649):
                orient_page_sizes = {"landscape": "SINGLE.LANDSCAPE"}
            else:
                orient_page_sizes = {"landscape": "DOUBLE.LANDSCAPE", "portrait": "DOUBLE.PORTRAIT"}
            orient = table_styles['x-sect-orient']
            if orient in orient_page_sizes:
                attrs['PAGE.SIZE'] = orient_page_sizes[orient]

        table_elem = etree.Element(u"TBL", attrib=attrs, nsmap=self.ns_map)

        self.build_corpus(table_elem, table)
        return table_elem

    def build_corpus(self, tbl_elem, table):
        """
        Build the Formex4 ``<CORPUS>`` element.

        :type  tbl_elem: etree._Element
        :param tbl_elem: Parent element: ``<TBL>``.

        :type  table: benker.table.Table
        :param table: Table
        """
        table_styles = table.styles
        attrs = {}  # no attribute
        rows = list(table.rows)

        # Does the first row/cell contains a centered title?
        first_cell = table[(1, 1)]
        align = first_cell.styles.get('align')
        if first_cell.width == table.bounding_box.width and align == "center":
            # yes, we can generate the title
            self.build_title(tbl_elem, rows.pop(0))

        # support for CALS-like elements and attributes
        if self.use_cals:
            qname = self.get_cals_qname
            attrs[qname("frame")] = get_frame_attr(table_styles)
            self._table_colsep = attrs[qname('colsep')] = get_colsep_attr(table_styles) or "0"
            self._table_rowsep = attrs[qname('rowsep')] = get_rowsep_attr(table_styles) or "0"
            if table.nature is not None:
                attrs[qname('tabstyle')] = table.nature
            if 'x-sect-orient' in table_styles:
                attrs[qname('orient')] = {"landscape": "land", "portrait": "port"}[table_styles['x-sect-orient']]
            if 'x-sect-cols' in table_styles:
                attrs[qname('pgwide')] = "1" if table_styles['x-sect-cols'] == "1" else "0"
            if 'background-color' in table_styles:
                attrs[qname('bgcolor')] = table_styles['background-color']

        corpus_elem = etree.SubElement(tbl_elem, u"CORPUS", attrib=attrs)

        # support for CALS-like elements and attributes
        if self.use_cals:
            for col in table.cols:
                self.build_colspec(corpus_elem, col)

        for row in rows:
            self.build_row(corpus_elem, row)

    def build_title(self, tbl_elem, row):
        """
        Build the table title using the ``<TITLE>`` element.

        For instance:

        .. code-block:: xml

           <TITLE>
             <TI>
               <P>Table IV</P>
             </TI>
           </TITLE>

        :type  tbl_elem: etree._Element
        :param tbl_elem: Parent element: ``<TBL>``.

        :type  row: benker.table.RowView
        :param row: The row which contains the title.
        """
        title_elem = etree.SubElement(tbl_elem, u"TITLE")
        for cell in row.owned_cells:
            text = text_type(cell)
            if text:
                if isinstance(cell.content, type(u"")):
                    # mainly useful for unit test
                    ti_elem = etree.SubElement(title_elem, u"TI")
                    p_elem = etree.SubElement(ti_elem, u"P")
                    p_elem.text = cell.content
                else:
                    paragraphs = list(cell.content)
                    ti_elem = etree.SubElement(title_elem, u"TI")
                    ti_elem.append(paragraphs[0])
                    sti_elem = etree.SubElement(title_elem, u"STI")
                    sti_elem.extend(paragraphs[1:])
            else:
                # assert cell.content in {None, "", []}
                ti_elem = etree.SubElement(title_elem, u"TI")
                etree.SubElement(ti_elem, u"IE")

    def build_colspec(self, group_elem, col):
        """
        Build the CALS ``<colspec>`` element (only is *use_cals* is ``True``).

        CALS attributes:

        -   ``@colname`` is the column name. Its format is "c{col_pos}".

        -   ``@colwidth`` width of the column (with its unit).
            The unit is defined by the *width_unit* options.

        .. note::

           The ``@colnum`` attribute (number of column) is not generated
           because this value is usually implied, and can be deduce
           from the ``@colname`` attribute.

        :type  group_elem: etree._Element
        :param group_elem: Parent element: ``<tgroup>``.

        :type  col: benker.table.ColView
        :param col: Columns

        .. versionchanged:: 0.5.0
           Add support for CALS-like elements and attributes.
        """
        col_styles = col.styles
        qname = self.get_cals_qname
        attrs = {qname('colname'): u"c{0}".format(col.col_pos)}
        if 'width' in col_styles:
            width = col_styles['width']
            width, unit = re.findall(r"([+-]?(?:[0-9]*[.])?[0-9]+)(\w+)", width)[0]
            value = convert_value(float(width), unit, self.width_unit)
            attrs[qname('colwidth')] = u"{value:0.2f}{unit}".format(value=value, unit=self.width_unit)
        etree.SubElement(group_elem, qname(u"colspec"), attrib=attrs)

    def build_row(self, corpus_elem, row):
        """
        Build the Formex4 ``<ROW>`` element.

        Formex4 attributes:

        -   ``@TYPE`` The TYPE attribute indicates the specific role of the row in the table.
            The allowed values are:

            *   ALIAS: if the row contains aliases. Such references may be used when the table
                is included on several pages of a publication. The references are associated
                to column headers on the first page and are repeated on subsequent pages.
            *   HEADER: if the row contains cells which may be considered as a column header.
                This generally occurs for the first row of a table.
            *   NORMAL: if most of the cells of the row contain 'simple' or 'normal' data.
                This is the default value.
            *   NOTCOL: if the cells of the row contain units of measure relating to subsequent rows.
            *   TOTAL: if the row contains data which could be considered as 'totals'.

            Note that this TYPE attribute is also provided for the cells (CELL), which could
            be used to override the value defined for the row. On the other hand, 'NORMAL'
            is the default value, so it is necessary to specify the TYPE attribute value
            in each cell of a row which has a specific type in order to avoid the default
            overriding (see the first row of the example below).

        :type  corpus_elem: etree._Element
        :param corpus_elem: Parent element: ``<CORPUS>``.

        :type  row: benker.table.RowView
        :param row: The row.

        .. versionchanged:: 0.5.0
           Add support for CALS-like elements and attributes.
        """
        row_styles = row.styles
        attrs = {}
        nature_types = {"head": u"HEADER", "foot": u"TOTAL"}
        if row.nature in nature_types:
            attrs['TYPE'] = nature_types[row.nature]

        # support for CALS-like elements and attributes
        if self.use_cals:
            qname = self.get_cals_qname
            if 'valign' in row_styles:
                # same values as CSS/Properties/vertical-align
                # fmt: off
                attrs[qname('valign')] = {
                    'top': 'top',
                    'middle': 'middle',
                    'bottom': 'bottom',
                    'baseline': 'bottom',
                }[row_styles['valign']]
                # fmt: on

        if 'x-ins' in row_styles:
            # <?change-start change-id="ct140446841083680" type="row:insertion"
            #   creator="Anita BARREL" date="2017-11-15T11:46:00"?>
            rev_attrs = collections.OrderedDict({'type': 'row:insertion'})
            if 'x-ins-id' in row_styles:
                rev_attrs['change-id'] = "ct{0}".format(row_styles['x-ins-id'])
            if 'x-ins-author' in row_styles:
                rev_attrs['creator'] = row_styles['x-ins-author']
            if 'x-ins-date' in row_styles:
                rev_attrs['date'] = row_styles['x-ins-date']
            rev_pi = revision_mark("change-start", rev_attrs)
            corpus_elem.append(rev_pi)

        row_elem = etree.SubElement(corpus_elem, u"ROW", attrib=attrs)

        if 'x-ins' in row_styles:
            # <?change-end change-id="ct139821811327752" type="row:insertion"?>
            rev_attrs = collections.OrderedDict({'type': 'row:insertion'})
            if 'x-ins-id' in row_styles:
                rev_attrs['change-id'] = "ct{0}".format(row_styles['x-ins-id'])
            rev_pi = revision_mark('change-end', rev_attrs)
            corpus_elem.append(rev_pi)

        for cell in row.owned_cells:
            self.build_cell(row_elem, cell, row)

    # noinspection PyMethodMayBeStatic
    def build_cell(self, row_elem, cell, row):
        """
        Build the Formex4 ``<CELL>`` element.

        Formex4 attributes:

        -   ``@COL`` The mandatory COL attribute is used to specify in which column the cell is located.

        -   ``@COLSPAN`` When a cell in a row 'A' must be linked to a group of cells in the same row,
            the first CELL element of this group has to provide the COLSPAN attribute. The value of
            the COLSPAN attribute is the number of cells in the group. The COL attribute of the first
            cell indicates the number of the first column in the group.

            The use of the COLSPAN attribute is only allowed to relate the value of a cell in several
            columns within the same row. Its value must be at least equal to '2'.

        -   ``@ROWSPAN`` When a cell in column 'A' is linked to a cell in row 'B' located just below
            row 'A', the CELL element of this single cell must provide the ROWSPAN attribute.
            The value of the ROWSPAN attribute is equal to the number of cells in the group.
            The CELL element relating to the single cell must be placed within the first ROW element
            in the group. The ROW elements corresponding to the other rows in the group may not
            contain any CELL elements for the column containing the single cell 'A'.

            The use of the ROWSPAN attribute is only authorised to relate the value of a cell in several
            rows. Its value must be at least equal to '2'.

        -   ``@ACCH`` If the group of related cells is physically delimited by a horizontal brace,
            this symbol must be marked up using the ACCH attribute.

        -   ``@ACCV`` If the group of related cells is physically delimited by a vertical brace,
            this symbol must be marked up using the ACCV attribute.

        -   ``@TYPE`` The TYPE attribute of the CELL element is used to indicate locally the type
            of contents of the cells. It overrides the value of the TYPE attribute defined for
            the row (ROW) which contains the cell.

        :type  row_elem: etree._Element
        :param row_elem: Parent element: ``<ROW>``.

        :type  cell: benker.cell.Cell
        :param cell: The cell.

        :type  row: benker.table.RowView
        :param row: The parent row.

        .. versionchanged:: 0.5.0
           Add support for CALS-like elements and attributes.
           Add support for ``bgcolor`` (Table background color).
        """
        cell_styles = cell.styles
        attrs = {'COL': str(cell.box.min.x)}
        if cell.nature and cell.nature != row.nature:
            nature_types = {"head": u"HEADER", "body": u"NORMAL", "foot": u"TOTAL"}
            attrs['TYPE'] = nature_types[cell.nature]
        if cell.width > 1:
            attrs[u"COLSPAN"] = str(cell.width)
        if cell.height > 1:
            attrs[u"ROWSPAN"] = str(cell.height)

        # support for CALS-like elements and attributes
        if self.use_cals:
            qname = self.get_cals_qname
            if cell.box.max.x != self._table.bounding_box.max.x:
                # generate @colsep if the cell isn't in the last column
                cell_colsep = get_colsep_attr(cell_styles, "border-right")
                if cell_colsep and cell_colsep != self._table_colsep:
                    attrs[qname('colsep')] = cell_colsep
            if cell.box.max.y != self._table.bounding_box.max.y:
                # generate @rowsep if the cell isn't in the last row
                cell_rowsep = get_rowsep_attr(cell_styles, "border-bottom")
                if cell_rowsep and cell_rowsep != self._table_rowsep:
                    attrs[qname('rowsep')] = cell_rowsep
            if 'vertical-align' in cell_styles:
                # same values as CSS/Properties/vertical-align
                # 'w-both' is an extension of OoxmlParser
                attrs[qname('valign')] = {
                    'top': u'top',
                    'middle': u'middle',
                    'bottom': u'bottom',
                    'baseline': u'bottom',
                    'w-both': u'bottom',
                }[cell_styles['vertical-align']]
            if 'align' in cell_styles:
                # same values as CSS/Properties/text-align
                attrs[qname('align')] = {
                    'left': u'left',
                    'center': u'center',
                    'right': u'right',
                    'justify': u'justify',
                }[cell_styles['align']]
            if cell.width > 1:
                attrs[qname("namest")] = u"c{0}".format(cell.box.min.x)
                attrs[qname("nameend")] = u"c{0}".format(cell.box.max.x)
            if cell.height > 1:
                attrs[qname("morerows")] = str(cell.height - 1)
            if 'background-color' in cell_styles:
                attrs[qname('bgcolor')] = cell_styles['background-color']

        cell_elem = etree.SubElement(row_elem, u"CELL", attrib=attrs)
        text = text_type(cell)
        if text:
            if isinstance(cell.content, type(u"")):
                # mainly useful for unit test
                cell_elem.text = cell.content
            else:
                cell_elem.extend(cell.content)
        else:
            # The IE element is used to explicitly indicate
            # that specific structures have an empty content.
            etree.SubElement(cell_elem, u"IE")

    def finalize_tree(self, tree):
        """
        Finalize the resulting tree structure:
        calculate the ``@NO.SEQ`` values: sequence number of each table.

        :type  tree: etree._ElementTree
        :param tree: The resulting tree.
        """
        root = tree.getroot()
        context = iterwalk(root, events=('start',), tag=('TBL',))

        stack = []
        for action, elem in context:  # type: str, etree._Element
            elem_tag = elem.tag
            if elem_tag == 'TBL':
                elem_level = int(elem.xpath("count(ancestor-or-self::TBL)"))
                curr_level = len(stack)
                if curr_level < elem_level:
                    stack.extend([0] * (elem_level - curr_level))
                else:
                    stack[:] = stack[:elem_level]
                stack[elem_level - 1] += 1
                no_seq = u'.'.join(u"{:04d}".format(value) for value in stack)
                elem.attrib['NO.SEQ'] = no_seq
            else:
                raise NotImplementedError(elem_tag)
