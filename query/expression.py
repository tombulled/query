from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Final, Optional, final

from typing_extensions import Self

from query.constants import NO_VALUE, OPERATOR_PREFIX
from query.enums import ExpressionType
from query.errors import ParsingError
from query.types import NoValue


class Expression(ABC):
    @property
    @abstractmethod
    def type(self) -> ExpressionType:
        pass

    @staticmethod
    @abstractmethod
    def parse(self, value: Any, /) -> Self:
        raise NotImplementedError

    @abstractmethod
    def serialise(self) -> Any:
        raise NotImplementedError


class NoValueExpression(Expression):
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    @staticmethod
    def parse(value: Any, /) -> Self:
        if value != NO_VALUE:
            raise ParsingError(f"Expected no value, got {value!r}")
        return AlwaysTrue()

    def serialise(self) -> NoValue:
        return {OPERATOR_PREFIX + self.type.value: NO_VALUE}


class AlwaysTrue(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_TRUE


class AlwaysFalse(NoValueExpression):
    type: Final[ExpressionType] = ExpressionType.ALWAYS_FALSE


@dataclass
class FieldExpression(Expression, ABC):
    """
    A FieldExpression is an expression that acts on a field with syntax like:
        "field": {$operator: ...}
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
    # type: Final[ExpressionType] = ExpressionType.EXISTS
    type: ClassVar[ExpressionType] = ExpressionType.EXISTS
    exists: bool

    @staticmethod
    def parse(data: Any, /) -> Self:
        if not isinstance(data, bool):
            raise ParsingError(f"Expected data of type {bool}, got {type(data)}")
        return Exists(data)

    def serialise_rhs(self) -> Any:
        return {OPERATOR_PREFIX + self.type.value: self.exists}
