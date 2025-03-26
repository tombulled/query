from dataclasses import dataclass

from typing_extensions import Self

from query.expression import Expression
from query.expressions import *
from query.models import ExpressionInfo, SerialisationOptions
from query.parse import parse
from query.protocols import ParseExpression
from query.registry import ExpressionRegistry
from query.types import SerialisedExpression
from query.parse import EXPRESSION_BUILDERS

"""
# expressions = ExpressionRegistry(prefix="$")
# parser = ParseExpression(expressions)


expressions = Expressions(prefix="$")

@expressions("requirement")
class RequirementExpression(Expression):
    ...
"""


def serialise(expression: Expression, /) -> SerialisedExpression:
    return expression.serialise(SerialisationOptions())


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
s = serialise

d = parse({"$and": [{"name": {"$eq": "bob"}}, {"age": {"$gt": 25}}]})
d2 = parse({"name": "bob", "age": {"$gt": 25}})
