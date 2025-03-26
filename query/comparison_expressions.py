from dataclasses import dataclass
from typing import ClassVar, Final, Optional, Sequence

from typing_extensions import Self

from .api import Expression, ExpressionInfo, ExpressionParser, SerialisationOptions
from .types import Number, SerialisedExpression, Value
from .validators import validate_number, validate_value, validate_values

OPERATOR_PREFIX: Final[str] = "$"
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

    # NOTE: KEEP ME? ADD TO OTHERS?
    # def __repr__(self) -> str:
    #     return f"{type(self).__name__}({self.field!r}, {self.value!r})"

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        if options.implicit:
            return {self.field: self.value}

        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_value(info.argument))


@dataclass(frozen=True)
class Gt(Expression):
    operator: ClassVar[str] = "$gt"

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Gte(Expression):
    operator: ClassVar[str] = "$gte"

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class In(Expression):
    operator: ClassVar[str] = "$in"

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.values})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_values(info.argument))


@dataclass(frozen=True)
class Lt(Expression):
    operator: ClassVar[str] = "$lt"

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Lte(Expression):
    operator: ClassVar[str] = "$lte"

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Ne(Expression):
    operator: ClassVar[str] = "$ne"

    field: Optional[str]
    value: Number

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_number(info.argument))


@dataclass(frozen=True)
class Nin(Expression):
    operator: ClassVar[str] = "$nin"

    field: Optional[str]
    values: Sequence[Value]

    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.values})

    @classmethod
    def build(
        cls, info: ExpressionInfo, parse: ExpressionParser
    ) -> Self:
        return cls(info.field, validate_values(info.argument))
