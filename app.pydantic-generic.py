from typing import Annotated, Any, Generator, Generic, TypeVar

import humps
from pydantic import BaseModel, Field, PlainValidator

from query.constants import NO_VALUE
from query.types import NoValue

T = TypeVar("T")


def _validate_no_value(v: Any) -> NoValue:
    assert v == NO_VALUE
    return v


ValidatedNoValue = Annotated[NoValue, PlainValidator(_validate_no_value)]


class classproperty:
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class Expression(BaseModel, Generic[T]):
    value: T

    def __init__(self, value: T, /) -> None:
        super().__init__(value=value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    # def __rich_repr__(self) -> Generator[T, None, None]:
    #     yield self.value

    # @property
    @classproperty
    def name(cls) -> str:
        return humps.camelize(cls.__name__)


class NoValueExpression(Expression[ValidatedNoValue]):
    pass
    # value: ValidatedNoValue = Field(default_factory=lambda: NO_VALUE)
    # def __init__(self) -> None:
    #     super().__init__(NO_VALUE)


class AlwaysTrue(NoValueExpression):
    pass


class AlwaysFalse(NoValueExpression):
    pass


class BoolExpression(Expression[bool]):
    pass


def always_true() -> AlwaysTrue:
    return AlwaysTrue(NO_VALUE)


def always_false() -> AlwaysFalse:
    return AlwaysFalse(NO_VALUE)


# d = Expression[bool](value="fish")
d = BoolExpression(True)
# nv = NoValueExpression()
# nv = NoValueExpression({})
at = always_true()
af = always_false()
