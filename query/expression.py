from abc import ABC, abstractmethod
from typing import Any, Final

from typing_extensions import Self

from query.constants import NO_DATA, OPERATOR_PREFIX
from query.enums import ExpressionType
from query.errors import ParsingError
from query.types import NoData


class Expression(ABC):
    @property
    @abstractmethod
    def type(self) -> ExpressionType:
        pass

    @staticmethod
    @abstractmethod
    def parse(self, data: Any, /) -> Self:
        raise NotImplementedError

    @abstractmethod
    def serialise(self) -> Any:
        raise NotImplementedError


class NoValueExpression(Expression):
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    @staticmethod
    def parse(data: Any, /) -> Self:
        if data != NO_DATA:
            raise ParsingError(f"Expected no data, got {data!r}")
        return AlwaysTrue()

    def serialise(self) -> NoData:
        return {OPERATOR_PREFIX + self.type.value: NO_DATA}


class AlwaysTrue(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_TRUE


class AlwaysFalse(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_FALSE


# class Exists(Expression):
#     type: Final[ExpressionType] = ExpressionType.EXISTS
#     exists: bool

#     def __init__(self, exists: bool, /) -> None:
#         self.exists = exists

#     @staticmethod
#     def parse(data: Any, /) -> Self:
#         assert isinstance(data, bool)
#         return Exists(data)

#     def serialise(self) -> Any:
#         return {OPERATOR_PREFIX + self.type.value: self.exists}
