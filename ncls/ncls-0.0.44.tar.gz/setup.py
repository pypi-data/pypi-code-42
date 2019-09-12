from distutils.core import setup
from setuptools import find_packages, Extension, Command
from Cython.Build import cythonize

import os
import sys

CLASSIFIERS = """Development Status :: 5 - Production/Stable
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows :: Windows NT/2000
Operating System :: OS Independent
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: Unix
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics"""

# split into lines and filter empty ones
CLASSIFIERS = CLASSIFIERS.split("\n")

macros = [("CYTHON_TRACE", "1")]

# extension sources
macros = []

if macros:
    from Cython.Compiler.Options import get_directive_defaults
    directive_defaults = get_directive_defaults()
    directive_defaults['linetrace'] = True
    directive_defaults['binding'] = True

dir_path = os.path.dirname(os.path.realpath(__file__))

include_dirs = [dir_path + "/ncls/src", dir_path]

__version__ = open("ncls/version.py").readline().split(" = ")[1].replace(
    '"', '').strip()

extensions = [
    Extension(
        "ncls.src.ncls", ["ncls/src/ncls.pyx", "ncls/src/intervaldb.c"],
        define_macros=macros,
        include_dirs=include_dirs),
    Extension(
        "ncls.src.ncls32", ["ncls/src/ncls32.pyx", "ncls/src/intervaldb32.c"],
        define_macros=macros,
        include_dirs=include_dirs)
]

install_requires = ["cython", "numpy"]

setup(
    name = "ncls",
    version=__version__,
    packages=find_packages(),
    ext_modules = cythonize(extensions, language_level=2),
    install_requires = ["cython", "numpy"],
    # py_modules=["pyncls"],
    description = \
    'A wrapper for the nested containment list data structure.',
    long_description = __doc__,
    # I am the maintainer; the datastructure was invented by
    # Alexander V. Alekseyenko and Christopher J. Lee.
    author = "Endre Bakken Stovner",
    author_email='endrebak85@gmail.com',
    url = 'https://github.com/endrebak/ncls',
    license = 'New BSD License',
    classifiers = CLASSIFIERS,
    package_data={'': ['*.pyx', '*.pxd', '*.h', '*.c']},
    include_dirs=["."],
)
