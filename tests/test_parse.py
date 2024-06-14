from query import parse, eq
from query.builders import and_


def test_parse() -> None:
    assert parse({"name": "bob"}) == eq("name", "bob")
    assert parse({"name": "bob", "age": 43}) == and_(eq("name", "bob"), eq("age", 43))
  

    # assert parse({"$exists": True}) == {"operator": "exists", "data": True}
    # assert parse_expression({"name": {"$eq": "bob"}}) == {
    #     "operator": "eq",
    #     "data": {"field": "name", "value": "bob"},
    # }
    # assert parse_expression({"$and": []}) == {"operator": "and", "data": []}

    # assert parse({"name": "bob"}) == {"name": {"eq": "bob"}}

    # assert make_explicit({"name": "bob", "age": 10}) == {
    #     "$and": [{"name": {"eq": "bob"}}, {"age": {"eq": 10}}]
    # }
