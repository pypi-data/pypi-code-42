#! /usr/bin/env python

import argparse
import sys
import logging
from logging import config
from ndexutil.config import NDExUtilConfig
import ndexstringloader
import csv
import pandas as pd
from datetime import datetime
import gzip
import shutil
import os
from ndexutil.tsv.streamtsvloader import StreamTSVLoader
import requests
import ndex2

from uuid import UUID

logger = logging.getLogger(__name__)

SUCCESS_CODE = 0
ERROR_CODE = 2

STYLE = 'style.cx'

TSV2NICECXMODULE = 'ndexutil.tsv.tsv2nicecx2'

LOG_FORMAT = "%(asctime)-15s %(levelname)s %(relativeCreated)dms " \
             "%(filename)s::%(funcName)s():%(lineno)d %(message)s"


STRING_LOAD_PLAN = 'string_plan.json'
DEFAULT_ICONURL = 'https://home.ndexbio.org/img/STRING-logo.png'

def get_package_dir():
    """
    Gets directory where package is installed
    :return:
    """
    return os.path.dirname(ndexstringloader.__file__)

def get_load_plan():
    """
    Gets the load plan stored with this package
    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), STRING_LOAD_PLAN)

def get_style():
    """
    Gets the style stored with this package

    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), STYLE)

def _parse_arguments(desc, args):
    """
    Parses command line arguments
    :param desc:
    :param args:
    :return:
    """
    help_fm = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=help_fm)

    network_group = parser.add_mutually_exclusive_group()

    parser.add_argument('datadir', help='Directory where string '
                                        'data is downloaded to '
                                        'and processed from')
    parser.add_argument('--profile', help='Profile in configuration '
                                          'file to load '
                                          'NDEx credentials which means'
                                          'configuration under [XXX] will be'
                                          'used '
                                          '(default '
                                          'ndexstringloader)',
                        default='ndexstringloader')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat'
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')

    parser.add_argument('--conf', help='Configuration file to load '
                                       '(default ~/' +
                                       NDExUtilConfig.CONFIG_FILE)
    parser.add_argument('--loadplan', help='Load plan json file', default=get_load_plan())
    network_group.add_argument('--style', help='Path to NDEx CX file to use for styling networks', default=get_style())
    parser.add_argument('--iconurl', help='URL for __iconurl parameter '
                                          '(default ' + DEFAULT_ICONURL + ')',
                        default=DEFAULT_ICONURL)
    parser.add_argument('--cutoffscore', help='Sets cutoff score (default 0.7)',
                        type=float, default=0.7)
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module and'
                             'in ' + TSV2NICECXMODULE + '. Messages are '
                             'output at these python logging levels '
                             '-v = ERROR, -vv = WARNING, -vvv = INFO, '
                             '-vvvv = DEBUG, -vvvvv = NOTSET (default no '
                             'logging)')
    parser.add_argument('--skipdownload', action='store_true',
                        help='If set, skips download of data from string'
                             'and assumes data already resides in <datadir>'
                             'directory')

    network_group.add_argument('--template',  help='UUID of network to use for styling networks')

    parser.add_argument('--update', help='UUID of network to update')

    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' + ndexstringloader.__version__))

    parser.add_argument('--stringversion', help='Version of STRING DB (default 11.0)',
                        default='11.0')

    return parser.parse_args(args)


def _setup_logging(args):
    """
    Sets up logging based on parsed command line arguments.
    If args.logconf is set use that configuration otherwise look
    at args.verbose and set logging for this module and the one
    in ndexutil specified by TSV2NICECXMODULE constant
    :param args: parsed command line arguments from argparse
    :raises AttributeError: If args is None or args.logconf is None
    :return: None
    """

    if args.logconf is None:
        level = (50 - (10 * args.verbose))
        logging.basicConfig(format=LOG_FORMAT,
                            level=level)
        logging.getLogger(TSV2NICECXMODULE).setLevel(level)
        logger.setLevel(level)
        return

    # logconf was set use that file
    logging.config.fileConfig(args.logconf,
                              disable_existing_loggers=False)


class NDExSTRINGLoader(object):
    """
    Class to load content
    """
    def __init__(self, args):
        """
        :param args:
        """
        self._conf_file = args.conf
        self._profile = args.profile
        self._load_plan = args.loadplan
        self._string_version = args.stringversion
        self._args = args
        self._datadir = os.path.abspath(args.datadir)
        self._cutoffscore = args.cutoffscore
        self._iconurl = args.iconurl
        self._template = None
        self._ndex = None

        self._template_UUID = args.template
        self._update_UUID = args.update

        self._output_tsv_file_columns = [
            "name1",
            "represents1",
            "alias1",
            "name2",
            "represents2",
            "alias2",
            "neighborhood",
            "neighborhood_transferred",
            "fusion",
            "cooccurence",
            "homology",
            "coexpression",
            "coexpression_transferred",
            "experiments",
            "experiments_transferred",
            "database",
            "database_transferred",
            "textmining",
            "textmining_transferred",
            "combined_score"
        ]

        self._protein_links_url = \
            'https://stringdb-static.org/download/protein.links.full.v11.0/9606.protein.links.full.v11.0.txt.gz'

        self._names_file_url = \
            'https://string-db.org/mapping_files/STRING_display_names/human.name_2_string.tsv.gz'

        self._entrez_ids_file_url = \
            'https://stringdb-static.org/mapping_files/entrez/human.entrez_2_string.2018.tsv.gz'

        self._uniprot_ids_file_url = \
            'https://string-db.org/mapping_files/uniprot/human.uniprot_2_string.2018.tsv.gz'

        self._full_file_name = os.path.join(self._datadir, '9606.protein.links.full.v11.0.txt')
        self._entrez_file = os.path.join(self._datadir, 'entrez_2_string.2018.tsv')
        self._names_file = os.path.join(self._datadir, 'name_2_string.tsv')
        self._uniprot_file = os.path.join(self._datadir, 'uniprot_2_string.2018.tsv')
        self._output_tsv_file_name = os.path.join(self._datadir, '9606.protein.links.tsv')
        self._cx_network = os.path.join(self._datadir, '9606.protein.links.cx')

        self.ensembl_ids = {}
        self.duplicate_display_names = {}
        self.duplicate_uniprot_ids = {}


    def _parse_config(self):
        """
        Parses config
        :return:
        """
        ncon = NDExUtilConfig(conf_file=self._conf_file)
        con = ncon.get_config()
        self._user = con.get(self._profile, NDExUtilConfig.USER)
        self._pass = con.get(self._profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._profile, NDExUtilConfig.SERVER)


    def _load_style_template(self):
        """
        Loads the CX network specified by self._args.style into self._template
        :return:
        """
        self._template = ndex2.create_nice_cx_from_file(os.path.abspath(self._args.style))

    def _download(self, url, local_file_name):

        logger.info('downloading {} to {}...'.format(url, local_file_name))

        r = requests.get(url)
        if r.status_code != 200:
            return r.status_code

        with open(local_file_name, "wb") as code:
            code.write(r.content)
            logger.debug('downloaded {} to {}\n'.format(url, local_file_name))

        return SUCCESS_CODE

    def _unzip(self, zip_file):
        local_file_name = zip_file[:-3]

        logger.info('unzipping and then removing {}...'.format(zip_file))

        with gzip.open(zip_file, 'rb') as f_in:
            with open(local_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(zip_file)
        logger.debug('{} unzipped and removed\n'.format(zip_file))
        return SUCCESS_CODE

    def _download_STRING_files(self):
        """
        Parses config
        :return:
        """
        ret_code = self._download(self._protein_links_url, self._full_file_name + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ret_code

        ret_code = self._download(self._names_file_url, self._names_file + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ret_code

        ret_code = self._download(self._entrez_ids_file_url, self._entrez_file + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ret_code

        return self._download(self._uniprot_ids_file_url, self._uniprot_file + '.gz')

    def _unpack_STRING_files(self):
        """
        Parses config
        :return:
        """
        ret_code = self._unzip(self._full_file_name + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ERROR_CODE

        ret_code = self._unzip(self._entrez_file + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ERROR_CODE

        ret_code = self._unzip(self._names_file + '.gz')
        if (ret_code != SUCCESS_CODE):
            return ERROR_CODE

        return self._unzip(self._uniprot_file + '.gz')

    def _get_name_rep_alias(self, ensembl_protein_id):
        name_rep_alias = self.ensembl_ids[ensembl_protein_id]
        use_ensembl_id_for_represents = False

        if name_rep_alias['display_name'] is None:
            use_ensembl_id_for_represents = True
            name_rep_alias['display_name'] = 'ensembl:' + ensembl_protein_id.split('.')[1]

        if name_rep_alias['represents'] is None:
            if use_ensembl_id_for_represents:
                name_rep_alias['represents'] = name_rep_alias['display_name']
            else:
                name_rep_alias['represents'] = 'hgnc:' + name_rep_alias['display_name']

        if name_rep_alias['alias'] is None:
            if use_ensembl_id_for_represents:
                name_rep_alias['alias'] = name_rep_alias['display_name']
            else:
                name_rep_alias['alias'] = name_rep_alias['represents']

        ret_str = \
            name_rep_alias['display_name'] + '\t' + \
            name_rep_alias['represents'] + '\t' + \
            name_rep_alias['alias']

        return ret_str


    def check_if_edge_is_duplicate(self, edge_key_1, edge_key_2, edges, combined_score):
        is_duplicate = True

        if edge_key_1 in edges:
            if edges[edge_key_1] != combined_score:
                raise ValueError('duplicate edge with different scores found')

        elif edge_key_2 in edges:
            if edges[edge_key_2] != combined_score:
                raise ValueError('duplicate edge with different scores found')

        else:
            edges[edge_key_1] = combined_score
            is_duplicate = False

        return is_duplicate


    def create_output_tsv_file(self):

        # generate output tsv file
        output_file = self._output_tsv_file_name
        logger.debug('Creating target {} file...'.format(output_file))


        with open(output_file, 'w') as o_f:

            # write header to the output tsv file
            output_header = '\t'.join([x for x in self._output_tsv_file_columns]) + '\n'
            o_f.write(output_header)

            row_count = 1
            dup_count = 0
            cutoffscore_times_hundred = int(self._cutoffscore * 1000)

            edges = {}

            with open(self._full_file_name, 'r') as f_f:
                next(f_f)
                for line in f_f:
                    columns_in_row = line.split(' ')

                    combined_score = int(columns_in_row[-1].rstrip('\n'))

                    if combined_score >= cutoffscore_times_hundred:

                        protein1, protein2 = columns_in_row[0], columns_in_row[1]

                        edge_key_1 = (protein1, protein2)
                        edge_key_2 = (protein2, protein1)

                        if self.check_if_edge_is_duplicate(edge_key_1, edge_key_2, edges, combined_score):
                            dup_count += 1
                            continue

                        name_rep_alias_1 = self._get_name_rep_alias(protein1)
                        name_rep_alias_2 = self._get_name_rep_alias(protein2)

                        tsv_string = name_rep_alias_1 + '\t' + name_rep_alias_2 + '\t' + \
                                     '\t'.join(x for x in columns_in_row[2:])

                        o_f.write(tsv_string)
                        row_count += 1

        logger.debug('Created {} ({:,} lines) \n'.format(output_file, row_count))
        logger.debug('{:,} duplicate rows detected \n'.format(dup_count))


    def _check_if_data_dir_exists(self):
        data_dir_existed = True

        if not os.path.exists(self._datadir):
            data_dir_existed = False
            os.makedirs(self._datadir, mode=0o755)

        return data_dir_existed


    def _get_headers_headers_of_links_file(self):
        headers = None

        with open(self._full_file_name, 'r') as f:
            d_reader = csv.DictReader(f)
            headers = ((d_reader.fieldnames)[0]).split()

        return headers


    def _init_ensembl_ids(self):

        headers = self._get_headers_headers_of_links_file()

        logger.debug('Preparing a dictionary of Ensembl Ids ...')

        for i in range(2):
            df = pd.read_csv(self._full_file_name, sep='\s+', skipinitialspace=True, usecols=[headers[i]])
            df.sort_values(headers[i], inplace=True)
            df.drop_duplicates(subset=headers[i], keep='first', inplace=True)

            for index, row in df.iterrows():
                self.ensembl_ids[row[headers[i]]] = {}
                self.ensembl_ids[row[headers[i]]]['display_name'] = None
                self.ensembl_ids[row[headers[i]]]['alias'] = None
                self.ensembl_ids[row[headers[i]]]['represents'] = None

        logger.info('Found {:,} unique Ensembl Ids in {}\n'.format(len(self.ensembl_ids), self._full_file_name))



    def _populate_display_names(self):
        logger.debug('Populating display names from {}...'.format(self._names_file))
        row_count = 0

        with open(self._names_file, 'r') as f:
            next(f)
            row1 = csv.reader(f, delimiter=' ')
            for row in row1:
                columns_in_row = row[0].split()
                ensembl_id = columns_in_row[2]
                display_name = columns_in_row[1]

                if ensembl_id in self.ensembl_ids:

                    if (self.ensembl_ids[ensembl_id]['display_name'] is None):
                        self.ensembl_ids[ensembl_id]['display_name'] = display_name

                    elif display_name != self.ensembl_ids[ensembl_id]['display_name']:
                        # duplicate: we found entries in human.name_2_string.tsv where same Ensembl Id maps to
                        # multiple display name.  This should never happen though
                        if ensembl_id not in self.duplicate_display_names:
                            self.duplicate_display_names[ensembl_id] = []
                            self.duplicate_display_names[ensembl_id].append(self.ensembl_ids[ensembl_id]['display_name'])

                            self.duplicate_display_names[ensembl_id].append(display_name)

                row_count = row_count + 1;

        logger.debug('Populated {:,} display names from {}\n'.format(row_count, self._names_file))


    def _populate_aliases(self):
        logger.debug('Populating aliases from {}...'.format(self._entrez_file))
        row_count = 0

        with open(self._entrez_file, 'r') as f:
            next(f)
            row1 = csv.reader(f, delimiter=' ')
            for row in row1:
                columns_in_row = row[0].split()
                ensembl_id = columns_in_row[2]
                ncbi_gene_id = columns_in_row[1]

                if ensembl_id in self.ensembl_ids:

                    if (self.ensembl_ids[ensembl_id]['alias'] is None):

                        ensembl_alias = 'ensembl:' + ensembl_id.split('.')[1]

                        # ncbi_gene_id can be |-separated list, for example, '246721|548644'
                        ncbi_gene_id_split = ncbi_gene_id.split('|')

                        ncbi_gene_id_split = ['ncbigene:' + element + '|' for element in ncbi_gene_id_split]

                        if (len(ncbi_gene_id_split) > 1):
                            alias_string = "".join(ncbi_gene_id_split) + ensembl_alias
                        else:
                            alias_string = ncbi_gene_id_split[0] + ensembl_alias

                        self.ensembl_ids[ensembl_id]['alias'] = alias_string

                    else:
                        pass

                row_count = row_count + 1

        logger.debug('Populated {:,} aliases from {}\n'.format(row_count,
                                                               self._entrez_file))


    def _populate_represents(self):
        logger.debug('Populating represents from {}...'.format(self._uniprot_file))
        row_count = 0

        with open(self._uniprot_file, 'r') as f:
            row1 = csv.reader(f, delimiter=' ')
            for row in row1:
                columns_in_row = row[0].split()
                ensembl_id = columns_in_row[2]
                uniprot_id = columns_in_row[1].split('|')[0]

                if ensembl_id in self.ensembl_ids:

                    if (self.ensembl_ids[ensembl_id]['represents'] is None):
                        self.ensembl_ids[ensembl_id]['represents'] = 'uniprot:' + uniprot_id

                    elif uniprot_id != self.ensembl_ids[ensembl_id]['represents']:
                        # duplicate: we found entries in human.uniprot_2_string.tsv where same Ensembl Id maps to
                        # multiple uniprot ids.
                        if ensembl_id not in self.duplicate_uniprot_ids:
                            self.duplicate_uniprot_ids[ensembl_id] = []
                            self.duplicate_uniprot_ids[ensembl_id].append(self.ensembl_ids[ensembl_id]['represents'])

                            self.duplicate_uniprot_ids[ensembl_id].append('uniprot:' + uniprot_id)

                row_count = row_count + 1;

        logger.debug('Populated {:,} represents from {}\n'.format(row_count, self._uniprot_file))


    def _is_valid_update_UUID(self):
        is_valid = True

        if self._update_UUID is not None:
            try:
                uuid_obj = UUID(self._update_UUID)
                is_valid = str(uuid_obj) == self._update_UUID
            except ValueError:
                is_valid = False

        return is_valid


    def run(self):
        """
        Runs content loading for NDEx STRING Content Loader
        :param theargs:
        :return:
        """
        self._parse_config()
        self._load_style_template()

        if not self._is_valid_update_UUID():
           print('Invalid UUID value for {}: {}'.format('--update', self._update_UUID))
           return ERROR_CODE

        data_dir_existed = self._check_if_data_dir_exists()

        if self._args.skipdownload is False or data_dir_existed is False:
            ret_code = self._download_STRING_files()
            if ret_code != SUCCESS_CODE:
                return ERROR_CODE

            ret_code = self._unpack_STRING_files()
            if ret_code != SUCCESS_CODE:
                return ERROR_CODE

        self._init_ensembl_ids()

        #populate name - 4.display name -> becomes name
        self._populate_display_names()

        # populate alias - 3. node string id -> becomes alias, for example
        # ensembl:ENSP00000000233|ncbigene:857
        self._populate_aliases()

        self._populate_represents()

        self.create_output_tsv_file()

        return SUCCESS_CODE


    def _get_network_name(self):
        network_name = 'STRING - Human Protein Links - High Confidence'

        if self._cutoffscore > 0:
            network_name = network_name + ' (Score >= ' + str(self._cutoffscore) + ')'

        return network_name


    def _get_property_from_summary(self, property, summary, default_value):
        if summary is None:
            return default_value

        for prop in summary['properties']:
            if property == prop['predicateString']:
                if prop['dataType'] and prop['dataType'] == 'list_of_string':
                    string_value = prop['value'][1:-1]
                    string_value = string_value.replace('"', '')
                    return string_value.split(',')
                else:
                    return prop['value']

        return default_value





    def _init_network_attributes(self, summary=None):
        net_attributes = {}

        net_attributes['name'] = self._get_network_name() if summary is None else summary['name']

        net_attributes['description'] = '<br>This network contains high confidence (score >= ' \
                    + str(self._cutoffscore) + ') human protein links with combined scores. ' \
                    + 'Edge color was mapped to the combined score value using a gradient from light grey ' \
                    + '(low Score) to black (high Score).' if summary is None else summary['description']

        rights = 'Attribution 4.0 International (CC BY 4.0)'
        net_attributes['rights'] = self._get_property_from_summary('rights', summary, rights)

        rightsHolder = 'STRING CONSORTIUM'
        net_attributes['rightsHolder'] = self._get_property_from_summary('rightsHolder', summary, rightsHolder)

        net_attributes['version'] = self._string_version if summary is None else summary['version']

        organism = 'Homo sapiens (human)'
        net_attributes['organism'] = self._get_property_from_summary('organism', summary, organism)

        networkType = ['interactome', 'ppi']
        net_attributes['networkType'] = self._get_property_from_summary('networkType', summary, networkType)

        reference = '<p>Szklarczyk D, Morris JH, Cook H, Kuhn M, Wyder S, ' \
                    + 'Simonovic M, Santos A, Doncheva NT, Roth A, Bork P, Jensen LJ, von Mering C.<br><b> ' \
                    + 'The STRING database in 2017: quality-controlled protein-protein association networks, ' \
                    + 'made broadly accessible.</b><br>Nucleic Acids Res. 2017 Jan; ' \
                    + '45:D362-68.<br> <a target="_blank" href="https://doi.org/10.1093/nar/gkw937">' \
                    + 'DOI:10.1093/nar/gkw937</a></p>'
        net_attributes['reference'] = self._get_property_from_summary('reference', summary, reference)

        wasDerivedFrom = 'https://stringdb-static.org/download/protein.links.full.v11.0/9606.protein.links.full.v11.0.txt.gz'
        net_attributes['prov:wasDerivedFrom'] = self._get_property_from_summary('prov:wasDerivedFrom', summary, wasDerivedFrom)

        wasGeneratedBy = '<a href="https://github.com/ndexcontent/ndexstringloader" target="_blank">ndexstringloader ' \
            + str(ndexstringloader.__version__) + '</a>'
        net_attributes['prov:wasGeneratedBy'] = self._get_property_from_summary('prov:wasGeneratedBy', summary, wasGeneratedBy)

        __iconurl = self._iconurl
        net_attributes['__iconurl'] =  self._get_property_from_summary('__iconurl', summary, __iconurl)

        return net_attributes

    def _generate_CX_file(self, network_attributes):

        logger.debug('generating CX file for network {}...'.format(network_attributes['name']))

        with open(self._output_tsv_file_name, 'r') as tsvfile:

            with open(self._cx_network, "w") as out:
                loader = StreamTSVLoader(self._load_plan, self._template)

                loader.write_cx_network(tsvfile, out,
                    [
                        {'n': 'name', 'v': network_attributes['name']},
                        {'n': 'description', 'v': network_attributes['description']},
                        {'n': 'rights', 'v': network_attributes['rights']},
                        {'n': 'rightsHolder', 'v': network_attributes['rightsHolder']},
                        {'n': 'version', 'v': network_attributes['version']},
                        {'n': 'organism', 'v': network_attributes['organism']},
                        {'n': 'networkType', 'v': network_attributes['networkType'], 'd': 'list_of_string'},
                        {'n': 'reference', 'v': network_attributes['reference']},
                        {'n': 'prov:wasDerivedFrom', 'v': network_attributes['prov:wasDerivedFrom']},
                        {'n': 'prov:wasGeneratedBy', 'v': network_attributes['prov:wasGeneratedBy']},
                        {'n': '__iconurl', 'v': network_attributes['__iconurl']}
                    ])

        logger.debug('CX file for network {} generated\n'.format(network_attributes['name']))


    def _update_network_on_server(self, network_name, network_id=None):
        ret_code = SUCCESS_CODE
        logger.info('updating network {} on server {} '
                     'for user {}...'.format(network_name, str(self._server), str(self._user)))

        with open(self._cx_network, 'br') as network_out:
            try:
                ret_code = self._ndex.update_cx_network(network_out, network_id)
                logger.info('network {} updated on server {} for '
                            'user {}\n'.format(network_name, str(self._server), str(self._user)))
            except Exception as e:
                print('{}\n'.format(e))
                ret_code = ERROR_CODE

        return ret_code


    def _load_network_to_server(self, network_name):
        ret_code = SUCCESS_CODE
        logger.info('loading network {} to server {} '
                     'for user {}...'.format(network_name, str(self._server), str(self._user)))

        with open(self._cx_network, 'br') as network_out:
            try:
                self._ndex.save_cx_stream_as_new_network(network_out)
                logger.info('network {} saved on server {} for '
                            'user {}\n'.format(network_name, str(self._server), str(self._user)))
            except Exception as e:
                print('{}\n'.format(e))
                ret_code = ERROR_CODE

        return ret_code

    def set_ndex_connection(self, ndex):
        """
        Sets alternate connection to NDEx that will be
        returned by :py:func:`create_ndex_connection()`

        :param ndex: NDEx client
        :type ndex: :py:class:`~ndex2.client.Ndex`
        """
        self._ndex = ndex

    def create_ndex_connection(self):
        """
        Creates connection to NDEx server if one does not already exist
        The credentials are set via the configuration file which is parsed
        in run() method
        :return:
        """
        if self._ndex is None:
            try:
                self._ndex = ndex2.client.Ndex2(host=self._server, username=self._user, password=self._pass)

            except Exception as e:
                logger.exception('Caught exception: {}'.format(e))
                return None

        return self._ndex


    def get_network_summaries_from_NDEx_server(self):

        try:
            network_summaries = self._ndex.get_network_summaries_for_user(self._user)
        except Exception as e:
            print("\n{}: {}".format(type(e).__name__, e))
            return ERROR_CODE

        return network_summaries


    def get_network_uuid(self, network_name, network_summaries):

        for summary in network_summaries:
            network_name_1 = summary.get('name')

            if network_name_1 is not None:
                if network_name_1 == network_name:
                    return summary.get('externalId')

        return None


    def get_summary_from_summaries(self, summaries, network_UUID):
        for summary in summaries:
            if summary['externalId'] == network_UUID:
                return summary

        return None


    def get_template_from_server(self, summaries):
        template_summary = self.get_summary_from_summaries(summaries, self._template_UUID)

        if template_summary is None:
            print('Template network specified with --template {} not found for user {}'.format(self._template_UUID,
                                                                                               self._user))
            return ERROR_CODE

        try:
            self._template = ndex2.create_nice_cx_from_server(self._server, self._user, self._pass, self._template_UUID)
        except Exception as e:
            print("\n{}: {}".format(type(e).__name__, e))
            return ERROR_CODE

        return SUCCESS_CODE


    def prepare_CX(self, summaries=None, network_id=None):

        if summaries is None:
            network_summary = None
            network_attributes = self._init_network_attributes(network_summary)
        else:
            network_summary = self.get_summary_from_summaries(summaries, network_id)
            network_attributes = self._init_network_attributes(network_summary)

        self._generate_CX_file(network_attributes)


    def load_to_NDEx(self):

        # network is updated when:
        #  1. update UUID is specified and network with this UUID exists, or
        #  2. update UUID is not specified, but network with the name already exists
        #
        # network is created when:
        #  1. no update UUID is specified and network doesn't exist on server
        #
        # if update UUID is specified but network doesn't exist, quit

        if self.create_ndex_connection() is None:
            return ERROR_CODE

        network_name = self._get_network_name()

        summaries = self.get_network_summaries_from_NDEx_server()

        if summaries == ERROR_CODE:
            print('Unable to get network summaries for user {}'.format(self._user))
            return ERROR_CODE

        if self._template_UUID:
            # load template from server
            if self.get_template_from_server(summaries) == ERROR_CODE:
                return  ERROR_CODE

        if self._update_UUID:
            network_summary = self.get_summary_from_summaries(summaries, self._update_UUID)

            if network_summary is None:
                # warning that not found and ask if to create the network
                answer = None
                while answer not in ("y", "n"):
                    answer = input("Network with UUID {} not found on server; create a new one? Enter y or n: ".format(self._update_UUID))
                    if answer == "y":
                        self.prepare_CX()
                        return self._load_network_to_server(network_name)

                    elif answer == "n":
                        print('Bye')
                        return SUCCESS_CODE

            else:
                network_id = self.get_network_uuid(network_name, summaries)
                if network_id == ERROR_CODE:
                    return ERROR_CODE

                self.prepare_CX(summaries, network_id)
                return self._update_network_on_server(network_name, self._update_UUID)

        else:
            # update UUID not specified
            network_id = self.get_network_uuid(network_name, summaries)
            if network_id == ERROR_CODE:
                return ERROR_CODE

            if network_id is None:
                self.prepare_CX()
                return self._load_network_to_server(network_name)
            else:
                self.prepare_CX(summaries, network_id)
                return self._update_network_on_server(network_name, network_id)


def main(args):
    """
    Main entry point for program
    :param args:
    :return:
    """
    desc = """
    Version {version}

    Loads NDEx STRING Content Loader data into NDEx (http://ndexbio.org).

    To connect to NDEx server a configuration file must be passed
    into --conf parameter. If --conf is unset, the configuration
    ~/{confname} is examined.

    The configuration file should be formatted as follows:

    [<value in --profile (default dev)>]

    {user} = <NDEx username>
    {password} = <NDEx password>
    {server} = <NDEx server(omit http) ie public.ndexbio.org>


    """.format(confname=NDExUtilConfig.CONFIG_FILE,
               user=NDExUtilConfig.USER,
               password=NDExUtilConfig.PASSWORD,
               server=NDExUtilConfig.SERVER,
               version=ndexstringloader.__version__)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = ndexstringloader.__version__

    try:
        _setup_logging(theargs)
        loader = NDExSTRINGLoader(theargs)
        status_code = loader.run()
        if (status_code != SUCCESS_CODE):
            return ERROR_CODE
        return loader.load_to_NDEx()
    except Exception as e:
        print("\n{}: {}".format(type(e).__name__, e))
        return ERROR_CODE
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
