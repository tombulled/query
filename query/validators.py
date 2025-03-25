from typing import Any, Sequence

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

# def validate_expressions(value: Any)