from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ExpressionInfo:
    operator: str
    argument: Any
    field: Optional[str] = None


@dataclass
class SerialisationOptions:
    include_field: bool = True
    implicit: bool = (
        False  # mode = SIMPLE, COMPLEX, DEFAULT? (short, full, auto)
    )
