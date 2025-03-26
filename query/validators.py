from typing import Any, Callable, Sequence, Type, TypeVar

from .exceptions import ValidationError
from .expression import Expression
from .protocols import ParseExpression
from .types import Number, Value

T = TypeVar("T")


def _validate_sequence(
    value: Any, validate_item: Callable[[Any], T]
) -> Sequence[T]:
    if not isinstance(value, Sequence):
        raise ValidationError

    return tuple(map(validate_item, value))


def validate(value: Any, type_: Type[T], /) -> T:
    if not isinstance(value, type_):
        raise ValidationError

    return value


def validate_value(value: Any, /) -> Value:
    return value


def validate_values(value: Any, /) -> Sequence[Value]:
    return _validate_sequence(value, validate_value)


def validate_number(value: Any, /) -> Number:
    if not isinstance(value, (int, float)):
        raise ValidationError

    return value


def validate_expression(value: Any, parse: ParseExpression, /) -> Expression:
    return parse(value)


def validate_expressions(
    value: Any, parse: ParseExpression, /
) -> Sequence[Expression]:
    return _validate_sequence(
        value, lambda item: validate_expression(item, parse)
    )


def validate_boolean(value: Any, /) -> bool:
    return validate(value, bool)


def validate_string(value: Any, /) -> str:
    return validate(value, str)
