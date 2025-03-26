from abc import ABC, abstractmethod
from typing import Any, Protocol

from .models import ExpressionInfo, SerialisationOptions
from .types import SerialisedExpression


class ExpressionParser(Protocol):
    def __call__(self, value: Any, /) -> "Expression": ...


class ExpressionBuilder(Protocol):
    def __call__(
        self, info: ExpressionInfo, parse: "ExpressionParser"
    ) -> "Expression": ...


class Expression(ABC):
    @abstractmethod
    def serialise(
        self, options: SerialisationOptions, /
    ) -> SerialisedExpression:
        raise NotImplementedError
