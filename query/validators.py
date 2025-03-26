from typing import Any, Sequence

from .api import Expression, ExpressionParser
from .types import Number, Value


def validate_value(value: Any, /) -> Value:
    return value


def validate_values(value: Any, /) -> Sequence[Value]:
    if not isinstance(value, Sequence):
        raise TypeError

    return tuple(map(validate_value, value))


def validate_number(value: Any, /) -> Number:
    if not isinstance(value, (int, float)):
        raise TypeError

    return value


def validate_expression(value: Any, parse: ExpressionParser, /) -> Expression:
    return parse(value)


def validate_expressions(
    value: Any, parse: ExpressionParser, /
) -> Sequence[Expression]:
    if not isinstance(value, Sequence):
        raise TypeError

    return tuple(validate_expression(v, parse) for v in value)
