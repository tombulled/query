from dataclasses import dataclass
from typing import ClassVar, Optional, Sequence

from typing_extensions import Self

from .api import Expression
from .models import ExpressionInfo, SerialisationOptions
from .protocols import ExpressionParser
from .types import Number, SerialisedExpression, Value
from .utils import serialise_with_field, to_operator
from .validators import validate_number, validate_value, validate_values


@dataclass(frozen=True)
class Eq(Expression):
    operator: ClassVar[str] = to_operator("eq")

    field: Optional[str]
    value: Value

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        if options.implicit:
            return {self.field: self.value}

        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_value(info.argument))


@dataclass(frozen=True)
class Gt(Expression):
    operator: ClassVar[str] = to_operator("gt")

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Gte(Expression):
    operator: ClassVar[str] = to_operator("gte")

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class In(Expression):
    operator: ClassVar[str] = to_operator("in")

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.values})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_values(info.argument))


@dataclass(frozen=True)
class Lt(Expression):
    operator: ClassVar[str] = to_operator("lt")

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Lte(Expression):
    operator: ClassVar[str] = to_operator("lte")

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Ne(Expression):
    operator: ClassVar[str] = to_operator("ne")

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Nin(Expression):
    operator: ClassVar[str] = to_operator("nin")

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.values})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(info.field, validate_values(info.argument))
