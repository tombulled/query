from typing import Dict, Mapping, Sequence
from query.expression import EqualityMatchExpression, MatchExpression

expression_classes = {
    EqualityMatchExpression.k_name: EqualityMatchExpression,
}


def parse_value_or_expression(field, obj):
    return NotImplemented
    # if isinstance(obj, Dict):
    #     # If it's a literal map (no operators), return it.
    #     if not any(k.startswith("$") for k in obj.keys()):
    #         return Eq(field=field, operand=obj)

    #     return parse(obj, field=field)
    # else:
    #     # Literal value
    #     # return QueryOperator(operand=obj)
    #     return Eq(field=field, operand=obj)


def parse(expression) -> MatchExpression:
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
        op = expression_classes[key]
        # return QueryOperator(operator=operator, operand=parser(value, parse))
        # return op(operand=op.parse(value, None, parse))
        return op.parse(value)

    # The key is a field, so we need to parse the value.
    # If the value is an operator, we need to push the field.
    # If the operator is logical, we need to push the field to
    # all of the logical operator's operands
    query_part = parse_value_or_expression(key, value)
    # query_part.field = key
    return query_part
