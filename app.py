from abc import ABC
from abc import abstractmethod
from typing import TypeAlias, Any, Optional, TypeVar, Protocol
from enum import Enum
from dataclasses import dataclass

Value: TypeAlias = str

def validate_value(value: Any, /) -> Value:
    return value # TEMP NOOP


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
    # Comparison
    EQ = "$eq"
    # Logical
    AND = "$and"

T = TypeVar("T")

class ExpressionParser(Protocol):
    def __call__(self, operator: str, argument: Any, *, path: Optional[str] = None) -> "Expression":
        ...

# EXPRESSIONS = {
#     Operator.EQ: lambda
# }

class Expression(ABC):
    @abstractmethod
    def serialise(self) -> SerialisedExpression:
        raise NotImplementedError

class MyExpression(Expression):
    def serialise(self) -> SerialisedExpression:
        return {"$myExpression": "some-value"}

@dataclass(frozen=True)
class Eq(Expression):
    value: Value
    field: Optional[str] = None

    def __str__(self) -> str:
        field: str = self.field if self.field is not None else "???"

        return f"{field} == {self.value!r}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    def serialise(self) -> SerialisedExpression:
        serialised: SerialisedExpression = {Operator.EQ: self.value}

        if self.field is not None:
            serialised = {self.field: serialised}

        return serialised

    @staticmethod
    def parse(operator: str, argument: Any, *, path: Optional[str] = None) -> "Expression":
        assert path is not None
        value: Value = validate_value(argument)

        return Eq(field=path, value=value)

e = Eq("bob")
e2 = Eq("bob", "name")
