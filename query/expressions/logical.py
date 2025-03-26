from dataclasses import dataclass
from typing import Any, ClassVar, MutableMapping, Sequence

from typing_extensions import Self

from ..expression import Expression
from ..models import ExpressionInfo, SerialisationOptions
from ..protocols import ExpressionParser
from ..types import SerialisedExpression
from ..validators import validate_expressions


@dataclass(frozen=True)
class And(Expression):
    operator: ClassVar[str] = "$and"

    expressions: Sequence[Expression]

    def serialise(self, options: SerialisationOptions) -> SerialisedExpression:
        expressions: Sequence[SerialisedExpression] = [
            expression.serialise(options) for expression in self.expressions
        ]

        if options.implicit:
            serialised: MutableMapping[str, Any] = {}

            expression: SerialisedExpression
            for expression in expressions:
                serialised.update(expression)

            return serialised

        return {self.operator: expressions}

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(validate_expressions(info.argument, parse))
