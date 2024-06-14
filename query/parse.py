import dataclasses
from typing import Dict, Mapping, Sequence

from query.models import QueryPart
from query.types import Expression

from . import operators


def parse_value(value):
    return value


def parse_values(values):
    return values


def parse_boolean(value):
    assert isinstance(value, bool)

    return value


def parse_expressions(expressions):
    return [parse(expression) for expression in expressions]


parsers = {
    # Comparison Query Operators
    operators.Eq.operator: operators.Eq.parse,
    operators.Gt.operator: operators.Gt.parse,
    operators.Gte.operator: operators.Gte.parse,
    operators.In.operator: operators.In.parse,
    operators.Lt.operator: operators.Lt.parse,
    operators.Lte.operator: operators.Lte.parse,
    operators.Ne.operator: operators.Ne.parse,
    operators.Nin.operator: operators.Nin.parse,
    # Logical Query Operators
    operators.And.operator: operators.And.parse,
    # operators.Not.operator: operators.Not.parse,
    operators.Nor.operator: operators.Nor.parse,
    operators.Or.operator: operators.Or.parse,
    # Element Query Operators
    operators.Exists.operator: operators.Exists.parse,
    # "type": parse_type,
}


def parse_value_or_expression(obj) -> QueryPart:
    if isinstance(obj, Dict):
        # If it's a literal map (no operators), return it.
        if not any(k.startswith("$") for k in obj.keys()):
            return QueryPart(operator="eq", operand=obj)

        return parse(obj)
    else:
        # Literal value
        return QueryPart(operator="eq", operand=obj)

def parse(expression: Expression) -> QueryPart:
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
        parser = parsers[operator]
        return QueryPart(operator=operator, operand=parser(value, parse))

    query_part = parse_value_or_expression(value)
    return dataclasses.replace(query_part, field=key)
