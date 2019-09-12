# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['shreqt']

package_data = \
{'': ['*']}

install_requires = \
['pyexasol>=0.6.4,<0.7.0',
 'sqlalchemy-exasol>=2.0,<3.0',
 'sqlalchemy>=1.3,<2.0',
 'sqlparse>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'shreqt',
    'version': '0.4.0',
    'description': 'Query Testing framework',
    'long_description': '# ShreQT\n\n[![Build Status](https://travis-ci.org/karamazi/shreqt.svg?branch=master)](https://travis-ci.org/karamazi/shreqt)\n[![PyPi Version](https://img.shields.io/pypi/v/shreqt.svg?style=flat)](https://pypi.org/project/shreqt/)\n\n\n```\n⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆\n⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿\n⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀\n⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  Tests have layers\n⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  Ogres have layers\n⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀        ~ Anonymous\n⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉\n```\n\n# Overview\n\nQuery testing framework.\n\nCurrently supports only Exasol DB.\n\nThis project uses [Poetry](https://github.com/sdispater/poetry) for dependency management and packaging.\n\n# Development\n\nTo setup your virtual environment run the following command. The default location for poetry venvs is `~/Library/Caches/pypoetry/virtualenvs`\n\n```bash\npoetry install\n```\n\nTo run tests and lint checks:\n\n```bash\nmake checks\n```\n\nTo format on all files:\n\n```bash\nmake fmt\n```\n\n# Usage\n\n### Prequisite\n\nCurrently we only support Exasol connections.\nTo run local instance of Exasol as docker container run:\n\n```bash\ndocker run  -p 8999:8888 --detach --privileged --stop-timeout 120  exasol/docker-db:6.0.13-d1\n```\n\n_(MacOS)_ Keep in mind that Exasol is memory-heavy and you need to increase docker memory limit to at least `4GB`\n\n### Credentials\n\nShreQT uses following environment variables to connect to database.\n\n| Variable    | Default Value  |\n| ----------- | -------------- |\n| SHREQT_DSN  | localhost:8999 |\n| SHREQT_USER | sys            |\n| SHREQT_PASS | exasol         |\n\n## Example\n\nThe `example` directory contains simple example which illustrates the example usage.\n\n- `conftest.py` includes simple User schema and code which sets up the database for test session.\n- `example.py` includes a tested function.\n- `example_test.py` include example test function.\n\nYou can run the example with:\n\n```bash\nmake run-example\n```\n\n# Build && Deploy\n\nSetup `~/.pypirc` with credentials.\n\nRun checks and build package:\n\n```bash\nmake build\n```\n\nDeploy package to pypi using poetry:\n\n```bash\nmake deploy\n```\n\n### TODO\n\n- Automate deployment step with travis\n- Decorator functionality for temporary layer\n- Option to automatically clean layers up once dbonion is destroyed.\n- When exception is raised during layer insertion, whole layer should be rolled back before failure.\n',
    'author': 'Zibi Rzepka',
    'author_email': 'zibi.rzepka@revolut.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
