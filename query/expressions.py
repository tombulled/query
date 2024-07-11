from query.expression import Expression, NoValueExpression

# {"$alwaysTrue": {}}
class AlwaysTrue(NoValueExpression):
    pass

# {"$happy": True}
class Happy(Expression[bool]):
    pass


# {"$not": {...}}
class Not(Expression[Expression]):
    pass
