from typing import TypeVar
from query.expression import Eq, Exists
from query.types import Number, Value, Values

T = TypeVar("T")


def eq(field: str, value: T, /) -> Eq[T]:
    return Eq(field=field, value=value)


def gt(field: str, value: Number, /):
    raise NotImplementedError


def gte(field: str, value: Number, /):
    raise NotImplementedError


def in_(field: str, values: Values, /):
    raise NotImplementedError


def lt(field: str, value: Number, /):
    raise NotImplementedError


def lte(field: str, value: Number, /):
    raise NotImplementedError


def ne(field: str, value: Value, /):
    raise NotImplementedError


def nin(field: str, values: Values, /):
    raise NotImplementedError


def exists(field: str, exists: bool = True, /) -> Exists:
    return Exists(field=field, exists=exists)
