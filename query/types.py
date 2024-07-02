from typing import Any, Mapping, Sequence, TypeAlias, TypeVar, Union
from typing_extensions import Never

T = TypeVar("T")

Field = str
Value = Any
Values = Sequence[Value]

NoValue: TypeAlias = Mapping[Never, Never]
Expression: TypeAlias = Mapping[str, T]
Number: TypeAlias = Union[int, float]