from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Sequence

from typing_extensions import Self

from .api import Expression
from .types import SerialisedExpression


@dataclass(frozen=True)
class And(Expression):
    operator: ClassVar[str] = "$eq"

    expressions: Sequence[Expression]

    def serialise(self) -> SerialisedExpression:
        return {self.operator: tuple(map(Expression.serialise, self.expressions))}

    @classmethod
    def parse(
        cls, operator: str, argument: Any, *, field: Optional[str] = None
    ) -> Self:
        return cls(field, validate_expressions(argument))