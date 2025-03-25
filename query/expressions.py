from typing import Optional, Any, ClassVar, Final
from typing_extensions import Self
from dataclasses import dataclass
from .api import Expression
from .types import Value, SerialisedExpression, Number
from .validators import validate_value, validate_number

PLACEHOLDER: Final[str] = "???"

def with_field(field: Optional[str], expression: SerialisedExpression) -> SerialisedExpression:
    if field is None:
        return expression

    return {field: expression}

@dataclass(frozen=True)
class Eq(Expression):
    operator: ClassVar[str] = "$eq"

    field: Optional[str]
    value: Value

    # def __str__(self) -> str:
    #     field: str = self.field if self.field is not None else PLACEHOLDER

    #     return f"{field} == {self.value!r}"

    # def __repr__(self) -> str:
    #     return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @staticmethod
    def parse(
        operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Expression:
        return Eq(field, validate_value(argument))


@dataclass(frozen=True)
class Gt(Expression):
    operator: ClassVar[str] = "$gt"

    field: Optional[str]
    value: Number

    # def __str__(self) -> str:
    #     field: str = self.field if self.field is not None else PLACEHOLDER

    #     return f"{field} > {self.value}"

    # def __repr__(self) -> str:
    #     return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        return with_field(self.field, {self.operator: self.value})

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_number(argument))
