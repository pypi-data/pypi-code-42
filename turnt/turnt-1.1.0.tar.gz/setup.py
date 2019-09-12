#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

install_requires = \
['click', 'tomlkit']

entry_points = \
{'console_scripts': ['turnt = turnt:turnt']}

setup(name='turnt',
      version='1.1.0',
      description='Turnt is a simple expect-style testing tool for command-line',
      author='Adrian Sampson',
      author_email='asampson@cs.cornell.edu',
      url='https://github.com/cucapra/turnt',
      py_modules=['turnt'],
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.4',
     )
