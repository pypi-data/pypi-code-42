##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2018
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module checks that all the dependencies are installed properly.
"""

# System import
import importlib
import distutils

# Package import
from .info import __version__
from .info import REQUIRES
from .info import LICENSE
from .info import AUTHOR
from .utils import logo


def _check_python_versions():
    """ Check that all the Python dependencies are satisfied.

    A dependency is expected to be formatted as follows:
    <mod_name>>=<mod_min_version>

    Returns
    -------
    versions: dict with 2-uplet
        the minimum required version and the installed version for each module.
        '?' means no package found.
    """
    versions = {}
    for dependency in REQUIRES:
        if ">=" not in dependency:
            raise ValueError("'{0}' dependency no formatted correctly.".format(
                dependency))
        mod_name, mod_min_version = dependency.split(">=")
        try:
            mod_install_version = importlib.import_module(mod_name).__version__
        except:
            mod_install_version = "?"
        versions[mod_name] = (mod_min_version, mod_install_version)
    return versions


def info():
    """ Dispaly some usefull information about the package.

    Returns
    -------
    info: str
        package information.
    """
    dependencies = "Dependencies: \n"
    dependencies_info = _check_python_versions()
    for name, (min_version, install_version) in dependencies_info.items():
        dependencies += "{0:10s}: {1:9s} - required | {2:9s} installed".format(
            name, min_version, install_version)
        dependencies += "\n"
    version = "Package version: {0}\n".format(__version__)
    license = "License: {0}\n".format(LICENSE)
    authors = "Author: {0}\n\n".format(AUTHOR)
    return logo() + "\n\n" + version + license + authors + dependencies
