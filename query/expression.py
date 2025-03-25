from typing import Any, Callable, Dict, Generic, Iterable, Mapping, Sequence, Tuple, Type, TypeVar

import humps
from pydantic import BaseModel, Field, GetCoreSchemaHandler, model_serializer
from pydantic_core import CoreSchema, core_schema

from query.registry import EXPRESSIONS

T = TypeVar("T")


def _validate_expression(expression):
    print(f"Validating expression: {expression!r}")

    if isinstance(expression, Expression):
        return expression

    if not isinstance(expression, Mapping):
        raise Exception("Expression is not a map")

    keys: Sequence[str] = tuple(expression.keys())
    keys_len: int = len(keys)

    if keys_len == 0:
        raise Exception("No keys!")
    if keys_len > 1:
        values = [{k: v} for k, v in expression.items()]
        return _validate_expression({"$and": values})

    key: str = keys[0]
    value = expression[key]

    if not isinstance(key, str):
        raise Exception("Key is not a string")
    
    # If the key is an operator, we're already explicit, recurse.
    if key.startswith("$"):
        operator: str = key[1:]
        # op = expression_classes[key]
        op = EXPRESSIONS[operator]
        # return QueryOperator(operator=operator, operand=parser(value, parse))
        # return op(operand=op.parse(value, None, parse))
        # return op.parse(value)

        # raise NotImplementedError(f"Lookup {key!r} in registry and build using {value!r} - {op!r}")
        return op(value)
    
    raise NotImplementedError(f"Finish parsing for {key!r} and {value!r}")


# class Expression(BaseModel, ABC, Generic[T]):
class Expression(BaseModel, Generic[T]):
    value: T = Field(kw_only=False)

    def __init__(self, value: T, /) -> None:
        print(f"{type(self).__name__}.__init__({value!r})")
        super().__init__(value=value)
        # self.value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    def __repr_args__(self) -> Iterable[Tuple[str | None, Any]]:
        return ((None, self.value),)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_before_validator_function(
            _validate_expression, handler(source_type)
        )

    @model_serializer(mode="wrap")
    def serialize(self, handler) -> Dict[str, Any]:
        return {humps.camelize(type(self).__name__): handler(self)}
