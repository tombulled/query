from query.expression import *
from query.expressions import *

e = Expression(123)
at = AlwaysTrue({})
h = Happy(True)
d = h.model_dump()
