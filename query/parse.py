from dataclasses import dataclass
from typing import Any, Mapping, MutableSequence, Optional, Sequence

from .exceptions import ParseError
from .expression import Expression
from .expressions import And, Eq
from .models import ExpressionInfo
from .protocols import ExpressionBuilder
from .utils import is_operator, serialise_with_field

# EXPRESSION_BUILDERS: Mapping[str, ExpressionBuilder] = {
#     # Comparison
#     Eq.operator: Eq.build,
#     Gt.operator: Gt.build,
#     Gte.operator: Gte.build,
#     In.operator: In.build,
#     Lt.operator: Lt.build,
#     Lte.operator: Lte.build,
#     Ne.operator: Ne.build,
#     Nin.operator: Nin.build,
#     # Logical
#     And.operator: And.build,
#     # Element
#     Exists.operator: Exists.build,
#     Type.operator: Type.build,
# }


def _validate_keys(mapping: Mapping, /) -> Sequence[str]:
    keys: MutableSequence[str] = []

    for key in mapping:
        if not isinstance(key, str):
            raise ParseError(f"Mapping key {key!r} is not a string")

        keys.append(key)

    return keys


@dataclass
class ExpressionParser:
    expressions: Mapping[str, ExpressionBuilder]

    def _parse_value_or_expression(
        self, field: Optional[str], value: Any
    ) -> Expression:
        # 1. Expression
        if isinstance(value, Mapping) and any(
            isinstance(key, str) and is_operator(key) for key in value
        ):
            return self.parse(value, field=field)

        # 2. Literal value
        return self.parse(serialise_with_field(field, {Eq.operator: value}))

    def parse(
        self, expression: Any, /, *, field: Optional[str] = None
    ) -> Expression:
        # 1. Not a mapping
        if not isinstance(expression, Mapping):
            raise ParseError("Expression is not a mapping")

        # 2. Keys are not strings
        keys: Sequence[str] = _validate_keys(expression)

        # 3. No keys in mapping
        if len(keys) == 0:
            raise ParseError("Expression is an empty mapping (no keys)")

        # 4. Multiple keys in mapping - implicit and
        if len(keys) > 1:
            expressions: Sequence[Mapping[str, Any]] = [
                {k: v} for k, v in expression.items()
            ]

            return self.parse({And.operator: expressions})

        key: str = keys[0]
        value: Any = expression[key]

        # 5. Field expression
        if not is_operator(key):
            return self._parse_value_or_expression(key, value)

        expression_builder: ExpressionBuilder = self.expressions[key]

        info: ExpressionInfo = ExpressionInfo(
            operator=key,
            argument=value,
            field=field,
        )

        # 6. Explicit expression
        return expression_builder(info, self.parse)
