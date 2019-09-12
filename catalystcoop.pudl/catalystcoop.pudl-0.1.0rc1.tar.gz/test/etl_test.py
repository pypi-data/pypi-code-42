"""PyTest based testing of the FERC & PUDL Database initializations.

This module also contains fixtures for returning connections to the databases.
These connections can be either to the live databases for post-ETL testing or
to new temporary databases, which are created from scratch and dropped after
the tests have completed. See the --live_ferc_db and --live_pudl_db command
line options by running pytest --help. If you are using live databases, you
will need to tell PUDL where to find them with --pudl_in=<PUDL_IN>.

"""
import logging
import os
import os.path

import pudl
from pudl.convert.epacems_to_parquet import epacems_to_parquet

logger = logging.getLogger(__name__)


def test_ferc1_init_db(ferc1_engine):
    """
    Create a fresh FERC Form 1 DB and attempt to access it.

    If we are doing ETL (ingest) testing, then these databases are populated
    anew, in their *_test form.  If we're doing post-ETL (post-ingest) testing
    then we just grab a connection to the existing DB.

    Nothing needs to be in the body of this "test" because the database
    connections are created by the fixtures defined in conftest.py
    """
    pass


def test_pudl_init_db(ferc1_engine, pudl_engine):
    """
    Create a fresh PUDL DB and pull in some FERC1 & EIA data.

    If we are doing ETL (ingest) testing, then these databases are populated
    anew, in their *_test form.  If we're doing post-ETL (post-ingest) testing
    then we just grab a connection to the existing DB.

    Nothing needs to be in the body of this "test" because the database
    connections are created by the fixtures defined in conftest.py
    """
    pass


def test_epacems_to_parquet(pudl_engine,
                            pudl_settings_fixture,
                            data_scope,
                            fast_tests):
    """Attempt to convert a small amount of EPA CEMS data to parquet format."""
    epacems_to_parquet(
        epacems_years=data_scope['epacems_working_years'],
        epacems_states=data_scope['epacems_states'],
        data_dir=pudl_settings_fixture['data_dir'],
        out_dir=os.path.join(
            pudl_settings_fixture['parquet_dir'], 'epacems'),
        compression='snappy',
        pudl_engine=pudl_engine,
    )


def test_ferc1_lost_data(pudl_settings_fixture, data_scope):
    """
    Check to make sure we aren't missing any old FERC Form 1 tables or fields.

    Exhaustively enumerate all historical sets of FERC Form 1 database tables
    and their constituent fields. Check to make sure that the current database
    definition, based on the given reference year and our compilation of the
    DBF filename to table name mapping from 2015, includes every single table
    and field that appears in the historical FERC Form 1 data.

    """
    current_dbc_map = pudl.extract.ferc1.get_dbc_map(
        year=data_scope['refyear'],
        data_dir=pudl_settings_fixture['data_dir']
    )
    current_tables = list(current_dbc_map.keys())
    logger.info(f"Checking for new, unrecognized FERC1 "
                f"tables in {data_scope['refyear']}.")
    for table in current_tables:
        # First make sure there are new tables in refyear:
        if table not in pudl.constants.ferc1_tbl2dbf:
            raise AssertionError(
                f"New FERC Form 1 table '{table}' in {data_scope['refyear']} "
                f"does not exist in 2015 list of tables"
            )
    # Get all historical table collections...
    dbc_maps = {}
    for yr in data_scope['ferc1_data_years']:
        logger.info(f"Searching for lost FERC1 tables and fields in {yr}.")
        dbc_maps[yr] = pudl.extract.ferc1.get_dbc_map(
            year=yr,
            data_dir=pudl_settings_fixture['data_dir']
        )
        old_tables = list(dbc_maps[yr].keys())
        for table in old_tables:
            # Check to make sure there aren't any lost archaic tables:
            if table not in current_tables:
                raise AssertionError(
                    f"Long lost FERC1 table: '{table}' found in year {yr}. "
                    f"Refyear: {data_scope['refyear']}"
                )
            for field in dbc_maps[yr][table].values():
                if field not in current_dbc_map[table].values():
                    raise AssertionError(
                        f"Long lost FERC1 field '{field}' found in table "
                        f"'{table}' from year {yr}. "
                        f"Refyear: {data_scope['refyear']}"
                    )


def test_only_ferc1_pudl_init_db(data_scope,
                                 pudl_settings_fixture,
                                 live_ferc_db):
    """Verify that a minimal FERC Form 1 can be loaded without other data."""
    pudl.init.init_db(ferc1_tables=['plants_steam_ferc1', 'fuel_ferc1'],
                      ferc1_years=data_scope['ferc1_working_years'],
                      eia923_tables=[],
                      eia923_years=[],
                      eia860_tables=[],
                      eia860_years=[],
                      epacems_years=[],
                      epacems_states=[],
                      epaipm_tables=[],
                      pudl_settings=pudl_settings_fixture,
                      pudl_testing=True)

    # Grab a connection to the freshly populated PUDL DB
    pudl_engine = pudl.init.connect_db(
        pudl_settings=pudl_settings_fixture,
        testing=True
    )
    # So we can wipe it out before exiting the test.
    pudl.init.drop_tables(pudl_engine)
