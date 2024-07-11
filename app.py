from query import parse
from rich import print

# d = parse({"name": "tom", "age": 10})
# d = parse_expression({"name": "tom"  })


def t(v):
    print(f"{v!r} -> {parse(v)!r}")


# d = parse("value")
# d = parse(123)

# t("value")
# t(123)
t({"name": "Bob"})
t({"user": {"name": "Bob", "age": 53}})
t({"name": {"$eq": "Bob"}})
t({"name": {"$exists": True, "$eq": "Bob"}})
t({"name": "Bob", "age": 53})
t({"$exists": True})
t({"$exists": True, "$eq": "Bob"})
