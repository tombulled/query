from typing import Dict, Mapping, Optional, Sequence

from query.types import Expression

from .operators import (
    And,
    Eq,
    Exists,
    Gt,
    Gte,
    In,
    Lt,
    Lte,
    Ne,
    Nin,
    Nor,
    Or,
    QueryOperator,
)

ops = {
    # Comparison Query Operators
    Eq.operator: Eq,
    Gt.operator: Gt,
    Gte.operator: Gte,
    In.operator: In,
    Lt.operator: Lt,
    Lte.operator: Lte,
    Ne.operator: Ne,
    Nin.operator: Nin,
    # Logical Query Operators
    And.operator: And,
    # Not.operator: Not,
    Nor.operator: Nor,
    Or.operator: Or,
    # Element Query Operators
    Exists.operator: Exists,
    # "type": parse_type,
}


def parse_value_or_expression(field, obj) -> QueryOperator:
    if isinstance(obj, Dict):
        # If it's a literal map (no operators), return it.
        if not any(k.startswith("$") for k in obj.keys()):
            return Eq(field=field, operand=obj)

        return parse(obj, field=field)
    else:
        # Literal value
        # return QueryOperator(operand=obj)
        return Eq(field=field, operand=obj)


def parse(expression: Expression, field: Optional[str] = None) -> QueryOperator:
    if not isinstance(expression, Mapping):
        raise Exception("Expression is not a map")

    keys: Sequence[str] = tuple(expression.keys())
    keys_len: int = len(keys)

    if keys_len == 0:
        raise Exception("No keys!")
    if keys_len > 1:
        values = [{k: v} for k, v in expression.items()]
        return parse({"$and": values})

    key: str = keys[0]
    value = expression[key]

    if not isinstance(key, str):
        raise Exception("Key is not a string")

    # If the key is an operator, we're already explicit, recurse.
    if key.startswith("$"):
        operator: str = key[1:]
        op = ops[operator]
        # return QueryOperator(operator=operator, operand=parser(value, parse))
        # return op(operand=op.parse(value, None, parse))
        return op.parse(value, field, parse)

    # The key is a field, so we need to parse the value.
    # If the value is an operator, we need to push the field.
    # If the operator is logical, we need to push the field to
    # all of the logical operator's operands
    query_part = parse_value_or_expression(key, value)
    # query_part.field = key
    return query_part
