from query.expression import *
from query.expressions import *
from query.registry import EXPRESSIONS
from query.decorator import expression

# e = Expression(123)
# at = AlwaysTrue({})
# h = Happy(True)
# d = h.model_dump()


@expression
class Name(Expression[str]):
    pass



# d = Exists("name")
# d = Not(Exists(True))

d = Expression.model_validate({"$name": "Bob"})
# q = {"$not": {"$exists": True}}


