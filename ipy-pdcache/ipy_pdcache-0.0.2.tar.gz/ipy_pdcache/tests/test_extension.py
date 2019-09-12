import os

import pandas as pd

import pytest
from pandas.util.testing import assert_frame_equal
from IPython.testing.globalipapp import start_ipython


@pytest.fixture(scope='session')
def session_ip():
    """Yield interface to IPython."""
    yield start_ipython()


@pytest.fixture(scope='function')
def ip(session_ip):
    """Clean IPython between uses."""
    extension_list = ['ipy_pdcache']

    # load extensions
    for ext in extension_list:
        session_ip.run_line_magic(magic_name='load_ext', line=ext)

    yield session_ip

    # unload extensions
    for ext in extension_list:
        session_ip.run_line_magic(magic_name='unload_ext', line=ext)

    # clean state
    session_ip.run_line_magic(magic_name='reset', line='-f')


def test_basic_functionality(ip, tmp_path):
    fname = tmp_path / 'data.csv'

    # cache new data
    ip.run_cell_magic(magic_name='pdcache', line=f'df {fname}', cell="""
import pandas as pd
df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
    """)

    # test that data was saved correctly
    assert os.path.exists(fname)
    df = pd.read_csv(fname)
    assert_frame_equal(ip.user_global_ns['df'], df)

    # modify it, so we can test whether data loading works
    df['B'].iloc[1] = 42
    df.to_csv(fname, index=False)

    # load cached data
    ip.run_cell_magic(magic_name='pdcache', line=f'df_new {fname}', cell="""
import pandas as pd
df_new = pd.DataFrame({})
    """)

    # test that existing data cache was loaded
    assert_frame_equal(ip.user_global_ns['df_new'], df)
