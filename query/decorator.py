from typing import Optional, Type, TypeVar

import humps

from query.expression import Expression
from query.registry import EXPRESSIONS


E = TypeVar("E", bound="Type[Expression]")


def expression(cls, /, *, key: Optional[str] = None):
    if key is None:
        key = humps.camelize(cls.__name__)

    def wrapper(cls: E, /) -> E:
        setattr(cls, "key", key)

        EXPRESSIONS[key] = cls

        return cls

    if cls is None:
        return wrapper

    return wrapper(cls)
