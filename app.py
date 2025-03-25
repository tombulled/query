# from query.api import Operator
from query.expressions import Eq, Gt

EXPRESSIONS = {
    Eq.operator: Eq.parse,
    Gt.operator: Gt.parse,
}

e = Eq("bob")
e2 = Eq("bob", "name")
g = Gt(10)
g2 = Gt(10, "age")