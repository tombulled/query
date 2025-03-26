from abc import ABC, abstractmethod

from .models import SerialisationOptions
from .types import SerialisedExpression


class Expression(ABC):
    @abstractmethod
    def serialise(self, options: SerialisationOptions, /) -> SerialisedExpression:
        raise NotImplementedError
