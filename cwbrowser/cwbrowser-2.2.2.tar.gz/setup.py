#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
from setuptools import find_packages, setup


# Select appropriate modules
modules = []
for module in find_packages():
    if module.startswith("cwbrowser"):
        modules.append(module)

# Get the package meta information
release_info = {}
infopath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "cwbrowser", "info.py"))
with open(infopath) as open_file:
    exec(open_file.read(), release_info)

# Build the setup
setup(
    name=release_info["NAME"],
    description=release_info["DESCRIPTION"],
    long_description=release_info["LONG_DESCRIPTION"],
    license=release_info["LICENSE"],
    classifiers=release_info["CLASSIFIERS"],
    author=release_info["AUTHOR"],
    author_email=release_info["AUTHOR_EMAIL"],
    version=release_info["VERSION"],
    url=release_info["URL"],
    packages=modules,
    platforms=release_info["PLATFORMS"],
    extras_require=release_info["EXTRA_REQUIRES"],
    install_requires=release_info["REQUIRES"]
)
