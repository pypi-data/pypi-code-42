# pyre-unsafe
from typing import Any, Generic, TypeVar

from tools.pyre.pyre_extensions import GenericMeta


_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


class ParameterSpecificationComponentMeta(type):
    def __getitem__(cls, __tparams):
        return Any


class PositionalArgumentsOf(metaclass=ParameterSpecificationComponentMeta):
    pass


class KeywordArgumentsOf(metaclass=ParameterSpecificationComponentMeta):
    pass


class Map(Generic[_T1, _T2]):
    pass


class Concatenation(metaclass=GenericMeta):
    pass
