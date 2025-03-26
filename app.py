from typing import Any, Mapping, Sequence

from query.api import Expression, ExpressionBuilder, ExpressionInfo
from query.comparison_expressions import Eq, Gt, Gte, In, Lt, Lte, Ne, Nin
from query.logical_expressions import And

"""
{ <field> : { <operator> : <value> }}
"""

EXPRESSION_BUILDERS: Mapping[str, ExpressionBuilder] = {
    # Comparison
    Eq.operator: Eq.build,
    Gt.operator: Gt.build,
    Gte.operator: Gte.build,
    In.operator: In.build,
    Lt.operator: Lt.build,
    Lte.operator: Lte.build,
    Ne.operator: Ne.build,
    Nin.operator: Nin.build,
    # Logical
    And.operator: And.build,
}


def parse(value: Any, /) -> Expression:
    if not isinstance(value, Mapping):
        raise TypeError

    keys: Sequence[str] = tuple(value.keys())

    if len(keys) != 1:
        raise ValueError

    key: str = keys[0]
    val: Any = value[key]

    expression_builder: ExpressionBuilder = EXPRESSION_BUILDERS[key]

    info: ExpressionInfo = ExpressionInfo(
        operator=key,
        argument=val,
        field=None,
    )

    return expression_builder(info, parse)


eq = Eq("name", "bob")
gt = Gt("age", 10)
gte = Gte("age", 10)
in_ = In("name", ("bob", "sally"))
lt = Lt("age", 10)
lte = Lte("age", 10)
ne = Ne("age", 10)
nin = Nin("age", (10, 20))

d = parse({"$and": [{"$eq": "bob"}, {"$eq": "sally"}]})
