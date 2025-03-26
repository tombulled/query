from typing import Any, Sequence

from .api import Expression
from .protocols import ExpressionParser
from .types import Callable, Number, TypeVar, Value

T = TypeVar("T")


def _validate_sequence(value: Any, validate_item: Callable[[Any], T]) -> Sequence[T]:
    if not isinstance(value, Sequence):
        raise TypeError

    return tuple(map(validate_item, value))


def validate_value(value: Any, /) -> Value:
    return value


def validate_values(value: Any, /) -> Sequence[Value]:
    return _validate_sequence(value, validate_value)


def validate_number(value: Any, /) -> Number:
    if not isinstance(value, (int, float)):
        raise TypeError

    return value


def validate_expression(value: Any, parse: ExpressionParser, /) -> Expression:
    return parse(value)


def validate_expressions(
    value: Any, parse: ExpressionParser, /
) -> Sequence[Expression]:
    return _validate_sequence(value, lambda item: validate_expression(item, parse))
