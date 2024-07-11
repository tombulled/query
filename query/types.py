from typing import Any, Mapping, Sequence, TypeAlias, TypeVar, Union

from typing_extensions import Never

T = TypeVar("T")

NoValue: TypeAlias = Mapping[Never, Never]

Field = str
Value = Any
Values = Sequence[Value]
Number: TypeAlias = Union[int, float]

Expression: TypeAlias = Mapping[str, T]