from dataclasses import dataclass, field
from typing import Any, Callable, MutableMapping, Protocol, TypeVar

from .expression import Expression
from .protocols import ExpressionBuilder, ParseExpression
from .parse import ExpressionParser


class HasExpressionBuilder(Protocol):
    # @classmethod
    # def build(cls, info: ExpressionInfo, parse: ParseExpression) -> Self: ...
    build: ExpressionBuilder


E = TypeVar("E", bound=HasExpressionBuilder)


@dataclass
class Expressions:
    expressions: MutableMapping[str, ExpressionBuilder] = field(
        default_factory=dict
    )

    def __call__(self, operator: str, /) -> Callable[[E], E]:
        # TODO: Automatically prefix the operator with "$"?

        def decorate(expression_cls: E, /) -> E:
            self.register(operator, expression_cls.build)

            return expression_cls

        return decorate

    def register(
        self, operator: str, expression_builder: ExpressionBuilder
    ) -> None:
        self.expressions[operator] = expression_builder

    # @property
    # def parser(self) -> ExpressionParser:
    #     return ExpressionParser(self.expressions)

    def parse(self, expression: Any) -> Expression:
        return ExpressionParser(self.expressions).parse(expression)
