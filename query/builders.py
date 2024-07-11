from typing import TypeVar
from query.expressions import Happy
from query.types import Number, Value, Values

T = TypeVar("T")


def eq(field: str, value: Value, /):
    raise NotImplementedError


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


def exists(field: str, exists: bool = True, /) -> Happy:
    raise NotImplementedError
