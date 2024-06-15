from enum import Enum

__all__ = ("ExpressionType",)

class ExpressionType(Enum):
    # EQ: str = "eq"
    EXISTS: str = "exists"
    ALWAYS_TRUE: str = "alwaysTrue"
    ALWAYS_FALSE: str = "alwaysFalse"