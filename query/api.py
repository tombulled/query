from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Protocol, TypeVar

from .types import SerialisedExpression

T = TypeVar("T")


class StrEnum(str, Enum):
    pass


# class Operator(StrEnum):
#     # Comparison
#     EQ = "$eq"
#     # Logical
#     AND = "$and"


@dataclass
class ExpressionInfo:
    operator: str
    argument: Any
    field: Optional[str] = None


class ExpressionParser(Protocol):
    def __call__(self, value: Any, /) -> "Expression": ...


class ExpressionBuilder(Protocol):
    def __call__(
        self, info: ExpressionInfo, parse: "ExpressionParser"
    ) -> "Expression": ...


@dataclass
class SerialisationOptions:
    include_field: bool = True
    implicit: bool = False
    # mode = SIMPLE, COMPLEX, DEFAULT? (short, full, auto)


class Expression(ABC):
    @abstractmethod
    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        raise NotImplementedError
