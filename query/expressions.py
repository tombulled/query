from query.expression import Expression
from query.no_value_expression import NoValueExpression
from query.types import Number, Value, Values


# {"$eq": 123}
class Eq(Expression[Value]):
    pass


# {"$gt": 123}
class Gt(Expression[Number]):
    pass


# {"$gte": 123}
class Gte(Expression[Number]):
    pass


# {"$in": [123, 456]}
class In(Expression[Values]):
    pass


# {"$lt": 123}
class Lt(Expression[Number]):
    pass


# {"$lt": 123}
class Lte(Expression[Number]):
    pass


# {"$ne": 123}
class Ne(Expression[Value]):
    pass


# {"$nin": 123}
class Nin(Expression[Values]):
    pass


# {"$alwaysTrue": {}}
class AlwaysTrue(NoValueExpression):
    pass


# {"$happy": True}
class Happy(Expression[bool]):
    pass


# {"$exists": True}
class Exists(Expression[bool]):
    pass


# {"$not": {...}}
class Not(Expression[Expression]):
    pass
