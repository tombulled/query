from typing import Mapping, TypeAlias, TypeVar
from typing_extensions import Never

T = TypeVar("T")

NoValue: TypeAlias = Mapping[Never, Never]
Expression: TypeAlias = Mapping[str, T]
