from dataclasses import dataclass
from typing import ClassVar, Optional

from typing_extensions import Self

from ..expression import Expression
from ..models import ExpressionInfo, SerialisationOptions
from ..protocols import ParseExpression
from ..types import SerialisedExpression
from ..utils import serialise_with_field, to_operator
from ..validators import validate_boolean, validate_string


@dataclass(frozen=True)
class Exists(Expression):
    operator: ClassVar[str] = to_operator("exists")

    field: Optional[str]
    value: bool

    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ParseExpression) -> Self:
        return cls(info.field, validate_boolean(info.argument))


@dataclass(frozen=True)
class Type(Expression):
    operator: ClassVar[str] = to_operator("type")

    field: Optional[str]
    value: str

    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        return serialise_with_field(self.field, {self.operator: self.value})

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ParseExpression) -> Self:
        return cls(info.field, validate_string(info.argument))
