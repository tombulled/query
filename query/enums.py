from enum import Enum

__all__ = ("ExpressionType",)

class ExpressionType(Enum):
    # Comparison Operators
    EQ: str = "eq"

    # Element Operators
    EXISTS: str = "exists"

    # Boolean Expressions
    ALWAYS_TRUE: str = "alwaysTrue"
    ALWAYS_FALSE: str = "alwaysFalse"