from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from typing_extensions import Self

from query.expression import Expression
from query.manager import Expressions
from query.models import ExpressionInfo, SerialisationOptions
from query.protocols import ParseExpression
from query.types import SerialisedExpression
from query.utils import to_operator


def serialise(expression: Expression, /) -> SerialisedExpression:
    return expression.serialise(SerialisationOptions())


class ExpressionType(str, Enum):
    def __str__(self) -> str:
        return self.value

    REQUIREMENT = "requirement"


# expressions = ExpressionRegistry()
# parser = ParseExpression(expressions)
expressions = Expressions()


# @expressions(ExpressionType.REQUIREMENT)
@dataclass(frozen=True)
class RequirementExpression(Expression):
    operator: ClassVar[str] = to_operator("exists")

    requirement: str

    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        return {str(ExpressionType.REQUIREMENT): self.requirement}

    @classmethod
    def build(cls, info: ExpressionInfo, parse: ParseExpression) -> Self:
        assert info.field is None
        assert isinstance(info.argument, str)

        return cls(info.argument)


# TEMP
expressions.register("$requirement", RequirementExpression.build)
# EXPRESSION_BUILDERS["$requirement"] = RequirementExpression.build

p = expressions.parse
s = serialise

r = p({"$requirement": "1234"})
