from typing import Any
from .types import Value, Number

# def validate_path()

def validate_value(value: Any, /) -> Value:
    return value

def validate_number(value: Any, /) -> Number:
    if not isinstance(value, (int, float)):
        raise TypeError

    return value
