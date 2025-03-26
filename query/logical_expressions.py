from dataclasses import dataclass
from typing import ClassVar, Sequence

from typing_extensions import Self

from .api import (
    Expression,
    ExpressionInfo,
    ExpressionParser,
    SerialisationOptions,
)
from .types import SerialisedExpression
from .validators import validate_expressions


@dataclass(frozen=True)
class And(Expression):
    operator: ClassVar[str] = "$and"

    expressions: Sequence[Expression]

    # NOTE: KEEP ME? ADD TO OTHERS?
    # def __repr__(self) -> str:
    #     pretty_expressions: str = ", ".join(map(repr, self.expressions))

    #     return f"{type(self).__name__}({pretty_expressions})"

    def serialise(self, options: SerialisationOptions) -> SerialisedExpression:
        expressions: Sequence[SerialisedExpression] = [
            expression.serialise(options) for expression in self.expressions
        ]

        if options.implicit:
            return expressions
        else:
            return {self.operator: expressions}

        # return {
        #     # self.operator: tuple(expression.serialise() for expression in self.expressions)
        #     self.operator: [
        #         expression.serialise() for expression in self.expressions
        #     ]
        # }

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ExpressionParser) -> Self:
        return cls(validate_expressions(info.argument, parse))
