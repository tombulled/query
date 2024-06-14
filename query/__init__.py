from typing import Any, List, Mapping, Protocol, Sequence, Set, TypeVar


query = {"$and": [{"name": "tom"}]}

# exists: boolean
# {"$exists": {"field": "name", "exists": True}}
# {"name": {"$exists": True}}
# {"type": "exists", "data": {"field": "name", "value": True}}
# {""}

V = TypeVar("V")

Field = str
Value = str # Any
Expression = Mapping[str, Any] # WARN: Currently using Any

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

def parse_expression(expression: Expression):
  if not isinstance(expression, Mapping):
    raise Exception("Expression is not a map")
  
  keys: Sequence[str] = tuple(expression.keys())
  keys_len: int = len(keys)

  if keys_len == 0:
    raise Exception("No keys!")
  if keys_len > 1:
    values = [
      {k: v}
      for k, v in expression.items()
    ]
    return parse_expression({"$and": values})
  
  key: str = keys[0]
  value = expression[key]

  if not isinstance(key, str):
    raise Exception("Key is not a string")
  
  # If the key is a field
  # if not key.startswith("$"):

  # If the key is an operator, we're already explicit, recurse.
  if key.startswith("$"):
    operator: str = key[1:]
    return {"operator": operator, "data": parse_expression(value)} # TODO: Recurse!
  
  # Key is a field, we should contain >=1 element operators or a value
  # For now we just assume a value
  # operators = parse()
  # return parse({"$eq": [key, value]})
  # return parse_expression({"$eq": [{"$field": key}, {"$literal": value}]})
  return {"operator": "eq", "data": {"field": key, "value": value}}