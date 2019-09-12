#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['spooner']

package_data = \
{'': ['*']}

extras_require = \
{'test': ['pytest', 'pytest-cov', 'tox']}

setup(name='spooner',
      version='0.5',
      description='spooner',
      author='Danny McVey',
      author_email='',
      url='https://github.com/danmaps/spooner',
      packages=packages,
      package_data=package_data,
      extras_require=extras_require,
     )
