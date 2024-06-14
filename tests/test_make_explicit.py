from query import parse_expression


def test_make_explicit() -> None:
    assert parse_expression({"$exists": True}) == {"operator": "exists", "data": True}
    # assert parse_expression({"name": {"$eq": "bob"}}) == {
    #     "operator": "eq",
    #     "data": {"field": "name", "value": "bob"},
    # }
    # assert parse_expression({"name": "bob"}) == {"operator": "eq", "data": {"field": "name", "value": "bob"}}
    # assert parse_expression({"$and": []}) == {"operator": "and", "data": []}

    # assert parse({"name": "bob"}) == {"name": {"eq": "bob"}}

    # assert make_explicit({"name": "bob", "age": 10}) == {
    #     "$and": [{"name": {"eq": "bob"}}, {"age": {"eq": 10}}]
    # }
