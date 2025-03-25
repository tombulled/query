from typing import Optional, Any, ClassVar
from dataclasses import dataclass
from .api import Expression
from .types import Value, SerialisedExpression, Number
from .validators import validate_value, validate_number

@dataclass(frozen=True)
class Eq(Expression):
    operator: ClassVar[str] = "$eq"

    value: Value
    field: Optional[str] = None

    def __str__(self) -> str:
        field: str = self.field if self.field is not None else "???"

        return f"{field} == {self.value!r}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        serialised: SerialisedExpression = {Eq.operator: self.value}

        if self.field is not None:
            serialised = {self.field: serialised}

        return serialised

    @staticmethod
    def parse(operator: str, argument: Any, *, path: Optional[str] = None) -> Expression:
        # assert path is not None
        value: Value = validate_value(argument)

        return Eq(field=path, value=value)

@dataclass(frozen=True)
class Gt(Expression):
    operator: ClassVar[str] = "$gt"

    value: Number
    field: Optional[str] = None

    def __str__(self) -> str:
        field: str = self.field if self.field is not None else "???"

        return f"{field} > {self.value}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        serialised: SerialisedExpression = {Gt.operator: self.value}

        if self.field is not None:
            serialised = {self.field: serialised}

        return serialised

    @staticmethod
    def parse(operator: str, argument: Any, *, path: Optional[str] = None) -> Expression:
        # assert path is not None
        value: Number = validate_number(argument)

        return Gt(field=path, value=value,)