from dataclasses import dataclass
from typing import Any, ClassVar, Final, Optional, Sequence

from typing_extensions import Self

from .api import Expression
from .types import Number, SerialisedExpression, Value
from .validators import validate_number, validate_value, validate_values

PLACEHOLDER: Final[str] = "???"


def with_field(
    field: Optional[str], expression: SerialisedExpression
) -> SerialisedExpression:
    if field is None:
        return expression

    return {field: expression}


@dataclass(frozen=True)
class Eq(Expression):
    operator: ClassVar[str] = "$eq"

    field: Optional[str]
    value: Value

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_value(argument))


@dataclass(frozen=True)
class Gt(Expression):
    operator: ClassVar[str] = "$gt"

    field: Optional[str]
    value: Number

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))


@dataclass(frozen=True)
class Gte(Expression):
    operator: ClassVar[str] = "$gte"

    field: Optional[str]
    value: Number

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))


@dataclass(frozen=True)
class In(Expression):
    operator: ClassVar[str] = "$in"

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.values})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_values(argument))


@dataclass(frozen=True)
class Lt(Expression):
    operator: ClassVar[str] = "$lt"

    field: Optional[str]
    value: Number

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))


@dataclass(frozen=True)
class Lte(Expression):
    operator: ClassVar[str] = "$lte"

    field: Optional[str]
    value: Number

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))


@dataclass(frozen=True)
class Ne(Expression):
    operator: ClassVar[str] = "$ne"

    field: Optional[str]
    value: Number

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))


@dataclass(frozen=True)
class Nin(Expression):
    operator: ClassVar[str] = "$nin"

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.values})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_values(argument))
