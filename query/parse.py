from typing import Any, Mapping, MutableSequence, Optional, Sequence

from query.api import (
    Expression,
    ExpressionBuilder,
    ExpressionInfo,
)
from query.comparison_expressions import Eq, Gt, Gte, In, Lt, Lte, Ne, Nin
from query.logical_expressions import And

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


def _validate_keys(mapping: Mapping, /) -> Sequence[str]:
    keys: MutableSequence[str] = []

    for key in mapping:
        if not isinstance(key, str):
            raise TypeError

        keys.append(key)

    return keys


def _parse_value_or_expression(field: Optional[str], value: Any) -> Expression:
    # 1. Not a mapping - is a literal value
    if isinstance(value, Mapping) and any(
        isinstance(key, str) and key.startswith("$") for key in value
    ):
        return parse(value, field=field)

    # Literal value
    if field is None:
        return parse({Eq.operator: value})
    else:
        return parse({field: {Eq.operator: value}})


def parse(expression: Any, /, *, field: Optional[str] = None) -> Expression:
    # 1. Not a mapping
    if not isinstance(expression, Mapping):
        raise TypeError

    # 2. Keys are not strings
    keys: Sequence[str] = _validate_keys(expression)

    # 3. No keys in mapping
    if len(keys) == 0:
        raise ValueError
    # 4. Multiple keys in mapping - implicit and
    elif len(keys) > 1:
        expressions: Sequence[Mapping[str,]] = [
            {k: v} for k, v in expression.items()
        ]

        return parse({And.operator: expressions})

    key: str = keys[0]
    value: Any = expression[key]

    # 5. Field expression
    if not key.startswith("$"):
        return _parse_value_or_expression(key, value)

    expression_builder: ExpressionBuilder = EXPRESSION_BUILDERS[key]

    info: ExpressionInfo = ExpressionInfo(
        operator=key,
        argument=value,
        field=field,
    )

    # 6. Explicit expression
    return expression_builder(info, parse)
