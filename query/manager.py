from dataclasses import dataclass, field
from typing import Any, Callable, MutableMapping, Protocol, TypeVar

from .expression import Expression
from .parse import ExpressionParser
from .protocols import ExpressionBuilder


class HasExpressionBuilder(Protocol):
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

    def parse(self, expression: Any) -> Expression:
        return ExpressionParser(self.expressions).parse(expression)
