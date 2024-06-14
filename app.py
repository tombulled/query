from query import parse_expression
from rich import print

# d = parse({"name": "tom", "age": 10})
# d = parse_expression({"name": "tom"  })


def t(v):
    print(f"{v!r} -> {parse_expression(v)!r}")


# d = parse("value")
# d = parse(123)

# t("value")
# t(123)
t({"name": "Bob"})
t({"name": {"$eq": "Bob"}})
# t({"name": {"$exists": True, "$eq": "Bob"}})
# t({"name": "Bob", "age": 53})
# t({"$exists": True})
# t({"$exists": True, "$eq": "Bob"})