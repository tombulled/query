from query.expression import Expression
from query.expressions import *
from query.models import SerialisationOptions
from query.parse import parse
from query.types import SerialisedExpression


def serialise(expression: Expression, /) -> SerialisedExpression:
    return expression.serialise(SerialisationOptions())


# class Exists(Expression):
#     pass

eq = Eq("name", "bob")
gt = Gt("age", 10)
gte = Gte("age", 10)
in_ = In("name", ("bob", "sally"))
lt = Lt("age", 10)
lte = Lte("age", 10)
ne = Ne("age", 10)
nin = Nin("age", (10, 20))
exists = Exists("name", True)

p = parse
s = lambda e: e.serialise(SerialisationOptions())

d = parse({"$and": [{"name": {"$eq": "bob"}}, {"age": {"$gt": 25}}]})
d2 = parse({"name": "bob", "age": {"$gt": 25}})

# ----------------

# expressions = ExpressionRegistry()
