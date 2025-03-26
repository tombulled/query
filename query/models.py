from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ExpressionInfo:
    operator: str
    argument: Any
    field: Optional[str] = None


@dataclass
class SerialisationOptions:
    # Whether to include the field in the serialised output.
    # For example: {<field>: {$eq: <value>}} vs {$eq: <value>}
    include_field: bool = True
    # Whether to serialise into the implicit form of this expression.
    # For example: {<field>: <value>} is the implicit form of {<field>: {$eq: <value>}}
    implicit: bool = False
