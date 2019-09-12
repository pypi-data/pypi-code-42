from typing import Optional, Sequence, Union
import pandas as pd
from pyexlatex.models.item import Item
from pyexlatex.models.containeritem import ContainerItem
from mixins.repr import ReprMixin
from pyexlatex.table.models.panels.collection import PanelCollection
from pyexlatex.table.models.texgen.alignment import ColumnsAlignment, ColumnAlignment
from pyexlatex.table.logic.table.build import build_tabular_content_from_panel_collection
from pyexlatex.models.caption import Caption
from pyexlatex.models.format.breaks import LineBreak
from pyexlatex.texgen import _centering_str
from pyexlatex.models.document import Document
from pyexlatex.models.package import Package
from pyexlatex.models.landscape import Landscape
from pyexlatex.models.label import Label
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.table.models.data.table import DataTable


class TableNotes(TextAreaBase, ReprMixin):
    name = 'tablenotes'

    def __init__(self, contents: Union[str, Sequence[str]]):
        super().__init__(self.name, contents, env_modifiers=f'[para, flushleft]')


class Tabular(Item, ReprMixin):
    name = 'tabular'
    repr_cols = ['align']

    def __init__(self, content, align: Optional[ColumnsAlignment] = None):
        if not isinstance(content, (list, tuple)):
            content = [content]
        self.align = align if align is not None else ColumnsAlignment(
            num_columns=Tabular._get_num_columns_from_content(content)
        )
        # TODO: really this should be cmidrule and others that require booktabs, but need to get all nested table
        # TODO: structure aggregating data.
        self.add_package('booktabs')
        super().__init__(self.name, content, env_modifiers=self._wrap_with_braces(str(self.align)))

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, align: Optional[ColumnsAlignment] = None,
                 mid_rules=True):
        align = align if align is not None else ColumnsAlignment(num_columns=panel_collection.num_columns)
        obj = cls([[0]], align=align)  # dummy content
        obj.panel_collection = panel_collection
        obj.contents = build_tabular_content_from_panel_collection(panel_collection, mid_rule=mid_rules)

        return obj

    @classmethod
    def from_df(cls, df: pd.DataFrame, align: Optional[ColumnsAlignment] = None, **dt_from_df_kwargs):
        dt = DataTable.from_df(df, **dt_from_df_kwargs)
        return cls(dt, align=align)

    @staticmethod
    def _get_num_columns_from_content(content) -> int:
        # Content should be made a list before this function. Get first or only content back
        reference_content = content[0]

        # Try to get from num_columns attribute if it exists
        num_columns = getattr(reference_content, 'num_columns', None)
        if num_columns is not None:
            return num_columns

        # Otherwise, try to take the length of the first passed content
        return len(reference_content)


class ThreePartTable(Item, ReprMixin):
    name = 'threeparttable'
    repr_cols = ['caption']

    def __init__(self, table_content: Tabular, caption: Caption=None, below_text: TableNotes=None,
                 label: Optional[Label] = None):
        self.caption = caption
        items = [
            caption,
            table_content,
            below_text,
            label
        ]
        valid_items = [item for item in items if item is not None]

        content = LineBreak().join(valid_items)
        super().__init__(self.name, content)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={}, **kwargs):
        tabular = Tabular.from_panel_collection(panel_collection, **tabular_kwargs)

        if panel_collection.name is not None:
            caption = Caption(panel_collection.name)
        else:
            caption = None

        return cls(tabular, caption=caption, *args, **kwargs)

class Table(ContainerItem, Item, ReprMixin):
    name = 'table'
    repr_cols = ['caption']

    def __init__(self, three_part_table: ThreePartTable, centering=True, landscape=False):
        self.caption = three_part_table.caption
        self.landscape = landscape

        items = [
            _centering_str() if centering else None,
            three_part_table
        ]

        valid_items = [item for item in items if item is not None]

        content = LineBreak().join(valid_items)

        Item.__init__(self, self.name, content)

    def __str__(self):
        content_with_env = super().__str__()
        if self.landscape:
            content_with_env = Landscape().wrap(str(content_with_env))
        return content_with_env

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={},
                              three_part_table_kwargs={}, **kwargs):
        three_part_table = ThreePartTable.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            **three_part_table_kwargs
        )
        return cls(three_part_table, *args, **kwargs)

    @classmethod
    def from_table_model(cls, table, *args, **kwargs):
        from pyexlatex.table.models.table.table import Table as TableModel
        table: TableModel
        tabular = Tabular.from_panel_collection(
            table.panels,
            align=table.align,
            mid_rules=table.mid_rules
        )

        three_part_table = ThreePartTable(
            tabular,
            caption=table.caption,
            below_text=table.below_text,
            label=Label(table.label) if table.label else None
        )
        obj = cls(three_part_table, *args, landscape=table.landscape, **kwargs)
        obj.add_data_from_content(table)
        return obj



class LTable(Table):
    name = 'ltable'


class TableDocument(Document):

    def __init__(self, content: Table, packages: [Package]=None, landscape: bool=False):
        from pyexlatex.table.models.texgen.packages import default_packages

        if packages is None:
            packages = []

        packages += default_packages

        super().__init__(content, packages, landscape=landscape)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={},
                              three_part_table_kwargs={}, table_kwargs={}, **kwargs):
        table = Table.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            three_part_table_kwargs=three_part_table_kwargs,
            **table_kwargs
        )
        return cls(table, *args, **kwargs)

    @classmethod
    def from_table_model(cls, table, *args, **kwargs):
        from pyexlatex.table.models.table.table import Table as TableModel
        table: TableModel
        tex_table = Table.from_table_model(table, *args, **kwargs)
        obj = cls(tex_table, *args, **kwargs)
        obj.add_data_from_content(table)
        return obj
