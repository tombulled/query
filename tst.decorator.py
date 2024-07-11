from typing import ClassVar

"""
from query import ...

exists, bool

and, Sequence[...], parse_expression

class Exists(Expression[bool]):
  pass
  
Exists = Expression[bool]("exists")
"""


class Expression:
    id: ClassVar[str]


# @expression("exists")
class Exists(Expression):
    id = "exists"


@expression("exists")
def exists(exists: bool, /):
    return exists
