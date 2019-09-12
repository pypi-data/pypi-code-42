# coding=utf-8
from __future__ import absolute_import
from ._version import __version__

__title__ = "geetools"
__summary__ = "A set of useful tools to use with Google Earth Engine Python" \
              "API"
__uri__ = "http://geetools.readthedocs.io"

__author__ = "Rodrigo E. Principe"
__email__ = "fitoprincipe82@gmail.com"

__license__ = "MIT"
__copyright__ = "2017 Rodrigo E. Principe"

try:
    from . import tools, bitreader, cloud_mask, expressions, decision_tree,\
                  filters, indices, batch, algorithms, composite,\
                  manager, utils, collection
    from .ui import eprint
    from .tools.imagecollection import wrapper
    from .batch import Export, Import, Convert, Download
except ImportError:
    pass
