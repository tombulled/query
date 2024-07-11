from query.expression import Exists
from query.expression import AlwaysTrue

d = Exists("name", True)
# d = AlwaysTrue()

"""

class Fishy(Expression[bool]):
  pass

"""
