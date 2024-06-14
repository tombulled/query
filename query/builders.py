from query.operators import And, Eq, Exists, QueryOperator
from query.types import Value


def eq(field: str, value: Value) -> Eq:
    return Eq(field=field, operand=value)


def and_(*operators: QueryOperator) -> And:
    return And(operand=list(operators))


def exists(field: str, exists: bool = True) -> Exists:
    return Exists(field=field, operand=exists)
