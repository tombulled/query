from query.expression import (
    AndMatchExpression,
    EqualityMatchExpression,
    AlwaysFalseMatchExpression,
    AlwaysTrueMatchExpression,
)
from query.parse2 import parse

# doc = {
#     "name": "Bob",
#     "age": 43,
# }

# expr = EqualityMatchExpression("name", "Bob")
# af = AlwaysFalseMatchExpression()
# at = AlwaysTrueMatchExpression()

# q = AndMatchExpression(
#     [
#         EqualityMatchExpression("name", "Bob"),
#         EqualityMatchExpression("age", 43),
#     ]
# )
q = {"$eq": 123}

d = parse(q)