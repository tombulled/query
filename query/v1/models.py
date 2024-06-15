from dataclasses import dataclass
from typing import Any, Optional


@dataclass
# class QueryPart(Protocol[T]):
class QueryPart:
    operator: str
    operand: Any
    field: Optional[str] = None