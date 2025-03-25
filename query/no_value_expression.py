from typing import Annotated, Any, Union

from pydantic import Field, PlainValidator
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from query.constants import NO_VALUE
from query.expression import Expression
from query.types import NoValue


def _validate_no_value(value: Any, /) -> NoValue:
    assert value == NO_VALUE
    return value


ValidatedNoValue = Annotated[NoValue, PlainValidator(_validate_no_value)]


class NoValueExpression(Expression[ValidatedNoValue]):
    value: ValidatedNoValue = Field(kw_only=False, default_factory=lambda: NO_VALUE)

    def __init__(
        self, value: Union[NoValue, PydanticUndefinedType] = PydanticUndefined, /
    ) -> None:
        super().__init__(
            value if not isinstance(value, PydanticUndefinedType) else NO_VALUE
        )
