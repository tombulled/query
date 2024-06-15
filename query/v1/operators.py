from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Generic, List, Optional, TypeVar
from typing_extensions import Self

from query.errors import ParsingError
from query.models import QueryPart

from .types import Expression, Expressions, Value, Values

T = TypeVar("T")


@dataclass
class QueryOperator(ABC, Generic[T]):
    operator: ClassVar[str]
    operand: T

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.operand!r})"

    @classmethod
    def parse(
        cls,
        value: Any,
        field: Optional[str],
        parse_expression: Callable[[Expression], QueryPart],
        /,
    ) -> Self:
        assert field is None
        return cls(operand=value)


@dataclass
class FieldQueryOperator(QueryOperator[T], Generic[T]):
    field: Optional[str] = None

    def __repr__(self) -> str:
        if self.field is None:
            return super().__repr__()

        return f"{type(self).__name__}({self.field!r}, {self.operand!r})"


### Comparison Query Operators ###


class ComparisonQueryOperator(FieldQueryOperator[T], Generic[T]):
    pass


class Eq(ComparisonQueryOperator[Value]):
    operator = "eq"

    def __str__(self) -> str:
        return f"{self.field}={self.operand!r}"

    @classmethod
    def parse(cls, value: Any, field, _, /) -> Self:
        return cls(field=field, operand=value)


class Gt(ComparisonQueryOperator[Value]):
    operator = "gt"


class Gte(ComparisonQueryOperator[Value]):
    operator = "gte"


class In(ComparisonQueryOperator[Values]):
    operator = "in"


class Lt(ComparisonQueryOperator[Value]):
    operator = "lt"


class Lte(ComparisonQueryOperator[Value]):
    operator = "lte"


class Ne(ComparisonQueryOperator[Value]):
    operator = "ne"


class Nin(ComparisonQueryOperator[Values]):
    operator = "nin"


### Logical Query Operators ###


class LogicalQueryOperator(QueryOperator[T], Generic[T]):
    pass


class And(LogicalQueryOperator[List[QueryPart]]):
    operator = "and"

    def __str__(self) -> str:
        expression: str = f" {self.operator} ".join(map(str, self.operand))

        return f"({expression})"

    @classmethod
    def parse(
        cls,
        value: Any,
        field,
        parse_expression: Callable[[Expression, Optional[str]], QueryPart],
        /,
    ) -> Self:
        if not isinstance(value, list):
            raise ParsingError(
                f"{cls.operator!r} operator expected value of type {list}, got {type(value)}"
            )

        return cls(
            operand=[parse_expression(expression, field) for expression in value]
        )


# class Not(LogicalQueryOperator[OperatorExpression]):
#     operator = "not"


class Nor(LogicalQueryOperator[Expressions]):
    operator = "nor"


class Or(LogicalQueryOperator[Expressions]):
    operator = "or"


### ###


class Exists(FieldQueryOperator[bool]):
    operator = "exists"

    @classmethod
    def parse(cls, value: Any, field: str, _, /) -> Self:
        if not isinstance(value, bool):
            raise ParsingError(
                f"{cls.operator!r} operator expected value of type {bool}, got {type(value)}"
            )

        return cls(field=field, operand=value)
