from abc import ABC, abstractmethod
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


class ExpressionParser(Protocol):
    def __call__(
        self, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> "Expression": ...


class Expression(ABC):
    @abstractmethod
    def serialise(self) -> SerialisedExpression:
        raise NotImplementedError
