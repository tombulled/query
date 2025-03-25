from abc import ABC
from abc import abstractmethod
from typing import TypeAlias, Any, Optional, TypeVar, Protocol
from enum import Enum
from dataclasses import dataclass

Value: TypeAlias = str

"""

{ <operator>: [ <argument1>, <argument2> ... ] }
or:
{ <operator>: <argument> }

And: expression / operator / filter
$and: name / type / key / id / operator / operator type

"And":
    Name: And
    Type: Operator
# {
#     "type": "$and",
#     "name": "And",
#     "category": "Operator"
# }

{
    "type": "ALWAYS_BOOLEAN",
    "name": "$alwaysTrue",
}

type: unique identifier for the expression *type*
name: the name to use when serialising?

 vvv path
        vvv operator
             vvv argument
{name: {$eq: "bob"}}
simple:
{name: "bob"}

class Name(Expression):
    ...

name_eq_tom = Expression("$eq", "tom", path="name")
"""

SerialisedExpression: TypeAlias = Any # Temporarily very loose

class StrEnum(str, Enum):
    pass

class Operator(StrEnum):
    EQ = "$eq"

T = TypeVar("T")

class ExpressionBuilder(Protocol):
    def __call__(self, operator: str, argument: Any, *, path: Optional[str] = None) -> "Expression":
        ...

# EXPRESSION_BUILDERS = {
#     "$eq":
# }

# class Expression(Generic[T]):
#     operator: str
#     argument: T
#     path: Optional[str]

#     def __init__(self, operator: str, argument: T, *, path: Optional[str] = None) -> None:
#         self.operator = operator
#         self.argument = argument
#         self.path = path

#     def serialise(self, include_path: bool = True) -> SerialisedExpression:
#         serialised: SerialisedExpression = {self.operator: self.argument}

#         if include_path and self.path is not None:
#             serialised = {self.path: serialised}

#         return serialised

class Expression(ABC):
    # @abstractmethod
    # def operator(self) -> str:
    #     raise NotImplementedError

    # def path(self) -> Optional[str]:
    #     return None

    @abstractmethod
    # def serialise(self, include_path: bool = True) -> SerialisedExpression:
    def serialise(self) -> SerialisedExpression:
        raise NotImplementedError

# class EqExpression(Expression)
#     # @staticmethod
#     def operator(self) -> str:
#         return "$eq"

#     def serialise(self) -> SerialisedExpression:
#         return {}



# class AlwaysBooleanExpression(Expression):
#     pass

# class AlwaysTrueExpression(AlwaysBooleanExpression):
#     pass

class MyExpression(Expression):
    # def serialise(self, include_path: bool = True) -> SerialisedExpression:
    def serialise(self) -> SerialisedExpression:
        return {"$myExpression": "some-value"}

EQ = "$eq"

@dataclass(frozen=True)
class Eq:
    value: Value
    field: Optional[str] = None

    def __str__(self) -> str:
        field: str = self.field if self.field is not None else "???"

        return f"{field} == {self.value!r}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        serialised: SerialisedExpression = {EQ: self.value}

        if self.field is not None:
            serialised = {self.field: serialised}

        return serialised

# name_eq_tom = Expression("$eq", "tom", path="name")
# e = name_eq_tom
#
e = Eq("bob")
e2 = Eq("bob", "name")