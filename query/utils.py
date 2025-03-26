from typing import Optional

from .constants import OPERATOR_PREFIX
from .types import SerialisedExpression


def is_operator(string: str, /) -> bool:
    return string.startswith(OPERATOR_PREFIX)


def to_operator(string: str, /) -> str:
    return OPERATOR_PREFIX + string


def serialise_with_field(
    field: Optional[str], expression: SerialisedExpression
) -> SerialisedExpression:
    if field is None:
        return expression

    return {field: expression}
