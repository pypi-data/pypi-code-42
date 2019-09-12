#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['cloudsync',
 'cloudsync.providers',
 'cloudsync.sync',
 'cloudsync.tests',
 'cloudsync.tests.fixtures',
 'cloudsync.tests.providers']

package_data = \
{'': ['*'],
 'cloudsync.tests': ['.pytest_cache/*',
                     '.pytest_cache/v/*',
                     '.pytest_cache/v/cache/*']}

install_requires = \
['arrow', 'oauth2client', 'dataclasses', 'pystrict']

extras_require = \
{'dropbox': ['dropbox'],
 'gdrive': ['httplib2',
            'google-api-python-client',
            'google-auth-httplib2',
            'google-auth-oauthlib']}

entry_points = \
{'console_scripts': ['cloudsync = cloudsync:main',
                     'cloudsync-tests = cloudsync:test_main']}

setup(name='cloudsync',
      version='0.1.30',
      description='cloudsync enables simple cloud file-level sync with a variety of cloud providers',
      author='Atakama, LLC',
      author_email='dev-support@atakama.com',
      url='https://github.com/atakamallc/cloudsync',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
