from typing import Generic, TypeVar
from pydantic import Field, TypeAdapter
from pydantic.dataclasses import dataclass


T = TypeVar("T")


@dataclass
class Expression(Generic[T]):
    value: T

    # def __init__(self, value: T, /) -> None:
    # super().__init__(value)
    # self.value = value

class Happy(Expression[bool]):
    pass

# @dataclass
# class ChildException(ParentException):
#     custom_field: str = "child"


# assert ChildException().custom_field == "child"

validator = TypeAdapter(Expression[int])

# assert validator.validate_python({"value": None}).value is None

# e = Expression[int](123)
# e2 = Expression[int]("bob")
