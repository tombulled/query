# Good Ref: https://github.com/fresheneesz/mongo-parse

from dataclasses import dataclass
import dataclasses
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence, Set, TypeVar


@dataclass
class QueryPart:
    operator: str
    operand: Any  # Type me?
    field: Optional[str] = None


V = TypeVar("V")

Field = str
Value = str  # Any
Values = List[Value]
Expression = Mapping[str, Any]  # WARN: Currently using Any
Expressions = List[Expression]


class Operator(Protocol):
    operator: str
    arguments: List[Any]


# Comparison Query Operators
class ComparisonQueryOperatorData(Protocol[V]):
    field: Field
    value: V


EqValue = Value
EqData = ComparisonQueryOperatorData[EqValue]
InValue = List[Value]
InData = ComparisonQueryOperatorData[InValue]
NeValue = Value
NeData = ComparisonQueryOperatorData[NeValue]
NinValue = List[Value]
NinData = ComparisonQueryOperatorData[NinValue]


# Element Query Operators
class ElementQueryOperatorData(Protocol[V]):
    field: Field
    value: V


ExistsValue = bool
ExistsData = ElementQueryOperatorData[ExistsValue]
TypeValue = str
TypeData = ElementQueryOperatorData[TypeValue]

# def parse_argument(argument):
#   # TODO: Parse argument(s)
#   # E.g. parse_argument(1) -> 1

# TODO: Operators need to own parsing of their argument(s)
# As they know whether or not they can/do contain sub-operators
# E.g. $gt knows it's argument is a *value*, whereas $and knows
# it's argument is an expression(s)


class Parser(Protocol):
    def __call__(self, field: Optional[str], value): ...


def parse_value(value):
    return value


def parse_values(values):
    return values


def parse_boolean(value):
    assert isinstance(value, bool)

    return value


# def parse_field_value(field, value):
#     # For now assume if the value is a map it contains operators:
#     if isinstance(value, Mapping):
#         return parse_expression() # TODO

#     assert field is not None
#     return {"field": field, "value": value}


def parse_expressions(expressions):
    return [parse_expression(expression) for expression in expressions]


parsers = {
    # "exists": parse_field_value,
    # "eq": parse_field_value,
    # Comparison Query Operators
    "eq": parse_value,
    "gt": parse_value,
    "gte": parse_value,
    "in": parse_values,
    "lt": parse_value,
    "lte": parse_value,
    "ne": parse_value,
    "nin": parse_values,
    # Logical Query Operators
    "and": parse_expressions,
    # "not": parse_operator_expression,
    "nor": parse_expressions,
    "or": parse_expressions,
    # Element Query Operators
    "exists": parse_boolean,
    # "type": parse_type,
}

# def parse_expr(expression: Expression):


# def parse(obj):
def parse_value_or_expression(obj) -> QueryPart:
    if isinstance(obj, Dict):
        # If it's a literal map (no operators), return it.
        if not any(k.startswith("$") for k in obj.keys()):
            # return obj
            return QueryPart(operator="eq", operand=obj)

        return parse_expression(obj)

        # # Ensure all keys are operators
        # if not all(k.startswith("$") for k in obj.keys()):
        #     raise Exception("Expression contains non-operators")

        # # If there are multiple operators, *and* them together
        # if len(obj.keys()) > 1:
        #   values = [{k: v} for k, v in obj.items()]
        #   return parse({"$and": values})

        # key = list(obj.keys())[0]
        # value = obj[key]

        # return {"operator": key[1:], "data": parse(value)}
    # elif isinstance(obj, List):
    #     return NotImplemented
    else:
        # Literal value
        # return obj
        return QueryPart(operator="eq", operand=obj)


def parse_expression(expression: Expression) -> QueryPart:
    if not isinstance(expression, Mapping):
        raise Exception("Expression is not a map")

    keys: Sequence[str] = tuple(expression.keys())
    keys_len: int = len(keys)

    if keys_len == 0:
        raise Exception("No keys!")
    if keys_len > 1:
        values = [{k: v} for k, v in expression.items()]
        return parse_expression({"$and": values})

    key: str = keys[0]
    value = expression[key]

    if not isinstance(key, str):
        raise Exception("Key is not a string")

    # If the key is an operator, we're already explicit, recurse.
    if key.startswith("$"):
        operator: str = key[1:]
        parser = parsers[operator]
        # return {"operator": operator, "data": parse_expression(value)} # TODO: Recurse!
        # return {"operator": operator, "data": parser(None, value)}  # TODO: Recurse!
        # return {"operator": operator, "data": parser(value)}  # TODO: Recurse!
        return QueryPart(operator=operator, operand=parser(value))

    # Key is a field, we should contain >=1 element operators or a value
    # For now we just assume a value
    # operators = parse()
    # return parse({"$eq": [key, value]})
    # return parse_expression({"$eq": [{"$field": key}, {"$literal": value}]})

    # parser = parsers["eq"]
    # return {"operator": "eq", "data": parser(key, value)}
    # return {
    #     "operator": "eq",
    #     "data": {"field": key, "value": parse_value_or_expression(value)},
    # }
    # return QueryPart(
    #     operator="eq",
    #     operand={"field": key, "value": parse_value_or_expression(value)},
    # )
    # return QueryPart(
    #     operator="eq",
    #     operand=parse_value_or_expression(value),
    #     field=key,
    # )
    query_part = parse_value_or_expression(value)
    return dataclasses.replace(query_part, field=key)
