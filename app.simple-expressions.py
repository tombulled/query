from typing import Any, Generic, Mapping, TypeVar
import humps

from query.constants import NO_VALUE
from query.types import NoValue

Expr = Mapping[str, Any]

T = TypeVar("T")


class Expression(Generic[T]):
    value: T

    def __init__(self, value: T, /) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    @property
    def name(self) -> str:
        return humps.camelize(type(self).__name__)

    @property
    def key(self) -> str:
        return "$" + self.name

    # def parse(self, expression: Expr, /) -> Self:

    def ser(self) -> Expr:
        return {self.key: self.value}


class NoValueExpression(Expression[NoValue]):
    def __init__(self) -> None:
        super().__init__(NO_VALUE)


class FieldExpression(Expression[T]):
    field: str

    def __init__(self, field: str, value: T) -> None:
        super().__init__(value)

        self.field = field

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.field!r}, {self.value!r})"

    def ser(self) -> str:
        return {self.field: super().ser()}


class Eq(FieldExpression[T]):
    pass


class Exists(Expression[bool]):
    pass


class AlwaysTrue(NoValueExpression):
    pass


class AlwaysFalse(NoValueExpression):
    pass


e = Exists(False)
at = AlwaysTrue()
af = AlwaysFalse()
eq = Eq("name", "bob")
