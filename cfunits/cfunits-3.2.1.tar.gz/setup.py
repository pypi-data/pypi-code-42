from distutils.core import setup, Extension
from distutils.command.build import build
import os
import fnmatch
import sys
import imp
import re

def find_package_data_files(directory):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*'):
                filename = os.path.join(root, basename)
                yield filename.replace('cfunits/', '', 1)

def _read(fname):
    """Returns content of a file.

    """
    fpath = os.path.dirname(__file__)
    fpath = os.path.join(fpath, fname)
    with open(fpath, 'r') as file_:
        return file_.read()

def _get_version():
    """Returns library version by inspecting __init__.py file.

    """
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     _read("cfunits/__init__.py"),
                     re.MULTILINE).group(1)
      
version      = _get_version()
packages     = ['cfunits']
etc_files    = [f for f in find_package_data_files('cfunits/etc')]
test_files    = [f for f in find_package_data_files('cfunits/test')]

package_data = etc_files + test_files

#with open('README.md') as ldfile:
#    long_description = ldfile.read()

long_description = """*A python interface to UNIDATA's Udunits-2 library with CF
extensions*

**Note: Versions 3.0.0 and later are only compatible with version Python 3. Use version 1.9 for Python 2 compatibility.**

Store, combine and compare physical units and convert numeric values
to different units.

Units are as defined in `UNIDATA's Udunits-2 library
<http://www.unidata.ucar.edu/software/udunits/>`_, except for
reference time units (such as ``'days since 2000-12-1'`` in the
``'proleptic_gregorian'`` calendar), which are handled by the `cftime
python package <https://pypi.python.org/pypi/cftime>`_.

In addition, some units are either new to, modified from, or removed
from the standard Udunits-2 database in order to be more consistent
with the `CF conventions <http://cfconventions.org/>`_.

`Home page <https://bitbucket.org/cfpython/cfunits-python>`_

`Dependencies
<https://bitbucket.org/cfpython/cfunits-python/src/master/README.md>`_

`Changelog
<https://bitbucket.org/cfpython/cfunits-python/src/master/Changelog.md>`_

"""

# classifiers list at: https://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(name = "cfunits",
      long_description = long_description,
      version      = version,
      description  = "A python interface to UNIDATA's Udunits-2 package with CF extensions ",
      maintainer   = "David Hassell",
      author       = "David Hassell",
      maintainer_email = "david.hassell@ncas.ac.uk",
      author_email = "david.hassell@ncas.ac.uk",
      url          = "https://bitbucket.org/cfpython/cfunits-python",
      download_url = "https://bitbucket.org/cfpython/cfunits-python/downloads",
      platforms    = ["Linux", "MacOS"],
      license      = ["MIT"],
      keywords     = ['cf', 'udunits', 'UNIDATA', 'netcdf','data',
                      'science', 'oceanography', 'meteorology', 'climate'],
      classifiers  = ["Development Status :: 5 - Production/Stable",
                      "Intended Audience :: Science/Research", 
                      "License :: OSI Approved :: MIT License", 
                      "Topic :: Scientific/Engineering",
                      "Operating System :: MacOS",
                      "Operating System :: POSIX :: Linux",
                      "Programming Language :: Python :: 3",],
      packages     = ['cfunits'],
      package_data = {'cfunits': package_data},
      install_requires = [
          'cftime>=1.0.0',
          'numpy>=1.15',
      ],
  )
