from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Final, Generic, Optional, TypeVar, final

from typing_extensions import Self

from query.constants import NO_VALUE, OPERATOR_PREFIX
from query.enums import ExpressionType
from query.errors import ParsingError
from query.types import Expression, NoValue

T = TypeVar("T")


def build_expression(operator: str, value: Optional[Any] = None) -> Expression:
    return {OPERATOR_PREFIX + operator: value if value is not None else NO_VALUE}


class Expression(ABC):
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    @property
    @abstractmethod
    # def type(self) -> ExpressionType:
    def type(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse(self, value: Any, /) -> Self:
        raise NotImplementedError

    @abstractmethod
    def serialise(self) -> Any:
        raise NotImplementedError


class NoValueExpression(Expression):
    @staticmethod
    def parse(value: Any, /) -> Self:
        if value != NO_VALUE:
            raise ParsingError(f"Expected no value, got {value!r}")
        return AlwaysTrue()

    def serialise(self) -> NoValue:
        return build_expression(self.type.value)


class AlwaysTrue(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_TRUE


class AlwaysFalse(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_FALSE


@dataclass
class FieldExpression(Expression, ABC):
    """
    A FieldExpression is an expression that acts on a field with syntax like:
        "field": {"$operator": ...}
    """

    field: Optional[str]

    @abstractmethod
    def serialise_rhs(self) -> Any:
        raise NotImplementedError

    @final
    def serialise(self) -> Any:
        return {self.field: self.serialise_rhs()}


@dataclass
class Exists(FieldExpression):
    type: ClassVar[ExpressionType] = ExpressionType.EXISTS
    exists: bool

    @staticmethod
    def parse(data: Any, /) -> Self:
        if not isinstance(data, bool):
            raise ParsingError(f"Expected data of type {bool}, got {type(data)}")
        return Exists(data)

    def serialise_rhs(self) -> Any:
        return build_expression(self.type.value, self.exists)


@dataclass
class Eq(FieldExpression, Generic[T]):
    type: ClassVar[ExpressionType] = ExpressionType.EQ
    value: T

    @staticmethod
    def parse(data: T, /) -> "Eq[T]":
        return Eq(data)

    def serialise_rhs(self) -> Any:
        return build_expression(self.type.value, self.value)
