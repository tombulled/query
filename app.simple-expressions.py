from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, Optional, Type, TypeVar

import humps
from typing_extensions import Self

from query.constants import NO_VALUE
from query.types import NoValue

"""
{"$exists": True}
{"$eq": "bob"}
{"$and": [{"$exists": True}, {"$eq": "bob"}]}
"""

Expr = Mapping[str, Any]

T = TypeVar("T")


class Expression(ABC, Generic[T]):
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

    @classmethod
    @abstractmethod
    def parse(cls: Type[Self], value: Any, /) -> Self:
        raise NotImplementedError

    def validate(self) -> None:
        pass

    def serialise(self) -> Expr:
        return {self.key: self.value}


class NoValueExpression(Expression[NoValue]):
    def __init__(self) -> None:
        super().__init__(NO_VALUE)

    @classmethod
    def parse(cls: Type[Self], value: Any) -> Self:
        assert value == NO_VALUE

        return cls()


class FieldExpression(Expression[T]):
    """
    A FieldExpression is an expression that acts on a field with syntax like:
        "field": {"$operator": ...}
    """

    field: Optional[str]

    def __init__(self, field: Optional[str], value: T) -> None:
        super().__init__(value)

        self.field = field

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.field!r}, {self.value!r})"

    def serialise(self) -> Expr:
        return {self.field: super().serialise()}

    def validate(self) -> None:
        assert self.field is not None


class Eq(FieldExpression[Any]):
    @classmethod
    def parse(cls: Type[Self], value: Any, /) -> Self:
        return cls(None, value)


class Exists(FieldExpression[bool]):
    # class Exists(Expression[bool]):
    @classmethod
    def parse(cls: Type[Self], value: Any, /) -> Self:
        assert isinstance(value, bool)

        return cls(None, value)


class AlwaysTrue(NoValueExpression):
    pass


class AlwaysFalse(NoValueExpression):
    pass


def exists(field: str, exists: bool) -> Exists:
    return Exists(field, exists)


# {"$alwaysTrue": {}}
# {"name": {"$exists": True}}

# e = Exists("name", False)
e = exists("name", False)
# e = Exists(False)
at = AlwaysTrue()
af = AlwaysFalse()
eq = Eq("name", "bob")
e2 = Exists.parse(True)
at2 = AlwaysTrue.parse({})
