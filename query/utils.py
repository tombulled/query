from .constants import OPERATOR_PREFIX


def is_operator(string: str, /) -> bool:
    return string.startswith(OPERATOR_PREFIX)


def to_operator(string: str, /) -> str:
    return OPERATOR_PREFIX + string
