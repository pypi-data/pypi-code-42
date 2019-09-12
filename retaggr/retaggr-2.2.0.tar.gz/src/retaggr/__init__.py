from .core import ReverseSearch, ReverseResult
from .config import ReverseSearchConfig
from .errors import MissingAPIKeysException, NotAValidEngineException, NotAvailableSearchException, EngineCooldownException
from .engines import ImageResult

from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=2, minor=2, micro=0, releaselevel="final", serial=0)

__version__ = "{}.{}.{}".format(version_info.major, version_info.minor, version_info.micro)