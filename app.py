# from query.api import Operator
from query.expressions import Eq, Gt

EXPRESSIONS = {
    Eq.operator: Eq.parse,
    Gt.operator: Gt.parse,
}

e = Eq(None, "bob")
e2 = Eq("name", "bob")
g = Gt(None, 10)
g2 = Gt("age", 10)
