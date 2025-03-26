from typing import Any, Protocol

from .expression import Expression
from .models import ExpressionInfo


class ExpressionParser(Protocol):
    def __call__(self, value: Any, /) -> "Expression": ...


class ExpressionBuilder(Protocol):
    def __call__(
        self, info: ExpressionInfo, parse: "ExpressionParser"
    ) -> "Expression": ...
