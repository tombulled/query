from abc import ABC
from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import humps
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    PlainValidator,
    model_serializer,
)
from pydantic_core import (
    CoreSchema,
    PydanticUndefined,
    core_schema,
    PydanticUndefinedType,
)

from query.constants import NO_VALUE
from query.types import NoValue

T = TypeVar("T")


def _validate_no_value(value: Any, /) -> NoValue:
    assert value == NO_VALUE
    return value


ValidatedNoValue = Annotated[NoValue, PlainValidator(_validate_no_value)]

E = TypeVar("E", bound="Type[Expression]")


def expression(key: str, /) -> Callable[[E], E]:
    def wrapper(cls: E, /) -> E:
        setattr(cls, "key", key)

        return cls

    return wrapper


# class Expression(BaseModel, ABC, Generic[T]):
class Expression(BaseModel, Generic[T]):
    value: T = Field(kw_only=False)

    # WARN: Custom constructors are not inherited :(
    def __init__(self, value: T, /) -> None:
        super().__init__(value=value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    def __repr_args__(self) -> Iterable[Tuple[str | None, Any]]:
        return ((None, self.value),)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # print(f"Expression.__get_pydantic_core_schema__:", cls, source_type, handler)

        def _validate_expression(v):
            # print(f"Validating expression: {v!r}")
            return v

        # return core_schema.no_info_after_validator_function(_validate_expression, handler(str))
        return core_schema.no_info_before_validator_function(
            _validate_expression, handler(source_type)
        )

    # @classmethod
    # def of(cls, value: T, /):
    #     return cls(value=value)

    @model_serializer(mode="wrap")
    def serialize(self, handler) -> Dict[str, Any]:
        return {humps.camelize(type(self).__name__): handler(self)}


@expression("nov")
class NoValueExpression(Expression[ValidatedNoValue]):
    value: ValidatedNoValue = Field(default_factory=lambda: NO_VALUE)

    def __init__(
        self, value: Union[NoValue, PydanticUndefinedType] = PydanticUndefined, /
    ) -> None:
        super().__init__(
            value if not isinstance(value, PydanticUndefinedType) else NO_VALUE
        )
