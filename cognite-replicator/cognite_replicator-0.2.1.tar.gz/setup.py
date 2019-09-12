# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cognite', 'cognite.replicator']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['replicator = cognite.replicator.__main__:main']}

setup_kwargs = {
    'name': 'cognite-replicator',
    'version': '0.2.1',
    'description': 'Python package for replicating data across CDF tenants. Copyright 2019 Cognite AS',
    'long_description': '<a href="https://cognite.com/">\n    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />\n</a>\n\n# Cognite Python Replicator\n[![build](https://webhooks.dev.cognite.ai/build/buildStatus/icon?job=github-builds/cognite-replicator/master)](https://jenkins.cognite.ai/job/github-builds/job/cognite-replicator/job/master/)\n[![codecov](https://codecov.io/gh/cognitedata/cognite-replicator/branch/master/graph/badge.svg)](https://codecov.io/gh/cognitedata/cognite-replicator)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nCognite Replicator is a Python package for replicating data across Cognite Data Fusion (CDF) projects. This package is\nbuilt on top of the Cognite Python SDK.\n\nCopyright 2019 Cognite AS\n\n## Prerequisites\nIn order to start using the Replicator, you need:\n* Python3 (>= 3.6)\n* Cognite Python SDK\n* Two API keys, one for your source tenant and one for your destination tenant. Never include the API key directly in the code or upload the key to github. Instead, set the API key as an environment variable.\n\nThis is how you set the API key as an environment variable on Mac OS and Linux:\n```bash\n$ export COGNITE_SOURCE_API_KEY=<your source API key>\n$ export COGNITE_DESTINATION_API_KEY=<your destination API key>\n```\n\n## Installation\nThe replicator is currently distribuated as Python wheels, but it can also be executed as a standalone script.\n\nOn this GitHub-page under **release** can you find the `.whl` file. By clicking on the file, you will automatically download the file. Then go into Databricks and into your cluster. Click on **Libraries** and **Install New**.  Choose your library type to be a **Python Whl**. By clicking on the area **Drop WHL here** you can navigate to where you have your `.whl`-file (most likely in your dowloads folder). Choose the `.whl` file, let the new library install and you are ready to replicate!\n\n## Usage\n\n### Setup as Python library\n```python\nimport os\n\nfrom cognite.client import CogniteClient\nfrom cognite.replicator import assets, events, time_series, datapoints\n\nSRC_API_KEY = os.environ.get("COGNITE_SOURCE_API_KEY")\nDST_API_KEY = os.environ.get("COGNITE_DESTINATION_API_KEY")\nPROJECT_SRC = "Name of source tenant"\nPROJECT_DST = "Name of destination tenant"\nCLIENT_NAME = "cognite-replicator"\nBATCH_SIZE = 10000 # this is the max size of a batch to be posted\nNUM_THREADS= 10 # this is the max number of threads to be used\n\nCLIENT_SRC = CogniteClient(api_key=SRC_API_KEY, project=PROJECT_SRC, client_name=CLIENT_NAME)\nCLIENT_DST = CogniteClient(api_key=DST_API_KEY, project=PROJECT_DST, client_name=CLIENT_NAME, timeout=90)\n\nassets.replicate(CLIENT_SRC, CLIENT_DST)\nevents.replicate(CLIENT_SRC, CLIENT_DST, BATCH_SIZE, NUM_THREADS)\ntime_series.replicate(CLIENT_SRC, CLIENT_DST, BATCH_SIZE, NUM_THREADS)\ndatapoints.replicate(CLIENT_SRC, CLIENT_DST)\n```\n\n### Run it from databricks notebook\n```python\nimport os\nimport logging\n\nfrom cognite.client import CogniteClient\nfrom cognite.replicator import assets, configure_databricks_logger\n\nSRC_API_KEY = dbutils.secrets.get("cdf-api-keys", "source-tenant")\nDST_API_KEY = dbutils.secrets.get("cdf-api-keys", "destination-tenant")\n\nCLIENT_SRC = CogniteClient(api_key=SRC_API_KEY, client_name="cognite-replicator")\nCLIENT_DST = CogniteClient(api_key=DST_API_KEY, client_name="cognite-replicator")\n\nlogger = logging.getLogger(__name__)\n\nconfigure_databricks_logger(log_level=logging.INFO, logger=logger)\nassets.replicate(CLIENT_SRC, CLIENT_DST)\n```\n\n### Run it from command line\n```bash\npoetry run replicator -h\n```\n\n## Changelog\nWondering about upcoming or previous changes to the SDK? Take a look at the [CHANGELOG](https://github.com/cognitedata/cognite-replicator/blob/master/CHANGELOG.md).\n\n## Contributing\nWant to contribute? Check out [CONTRIBUTING](https://github.com/cognitedata/cognite-replicator/blob/master/CONTRIBUTING.md).\n',
    'author': 'Nina Odegard',
    'author_email': 'nina.odegard@cognite.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
