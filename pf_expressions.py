from dataclasses import dataclass
from typing import ClassVar, Final

from typing_extensions import Self

from query.expression import Expression
from query.manager import Expressions
from query.models import ExpressionInfo, SerialisationOptions
from query.protocols import ParseExpression
from query.types import SerialisedExpression
from query.utils import to_operator

EXPRESSIONS: Final[Expressions] = Expressions()


@dataclass(frozen=True)
class RequirementExpression(Expression):
    operator: ClassVar[str] = to_operator("requirement")

    requirement: str

    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        return {self.operator: self.requirement}

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ParseExpression) -> Self:
        assert info.field is None
        assert isinstance(info.argument, str)

        return cls(info.argument)


EXPRESSIONS.register(
    RequirementExpression.operator, RequirementExpression.build
)
