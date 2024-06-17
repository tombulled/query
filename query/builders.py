from typing import TypeVar
from query.expression import Eq, Exists

T = TypeVar("T")


def eq(field: str, value: T) -> Eq[T]:
    return Eq(field=field, value=value)


def exists(field: str, exists: bool = True) -> Exists:
    return Exists(field=field, exists=exists)
