from typing import Any, Generic, TypeVar
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    SkipValidation,
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
)
from pydantic_core import CoreSchema, core_schema

"""
https://github.com/pydantic/pydantic/discussions/7008
"""

T = TypeVar("T")

# def validate(v):
#     key = next(iter(v.keys()))
#     val = v[key]

#     print(key, val)

#     assert key == "$happy"

#     # return Happy.model_validate({"value": val})
#     return Happy.model_validate({"value": val})


# def validate(
#     input_value: Any, validator: ValidatorFunctionWrapHandler, info: ValidationInfo, /
# ) -> Any:
#     print("validate:", input_value, validator, info)
#     title = info.config["title"]
#     print()

#     if title == "Expression":
#         key = next(iter(input_value.keys()))
#         val = input_value[key]

#         assert key == "$happy"

#         # return Happy.model_validate({"value": val})
#         return Happy(value=val)

#     # return {"value": input_value}
#     # return input_value
#     return validator(input_value)


def validate_expr(
    input_value: Any, validator: ValidatorFunctionWrapHandler, info: ValidationInfo, /
) -> Any:
    key = next(iter(input_value.keys()))
    val = input_value[key]

    assert key == "$happy"

    return Happy(value=val)


class Expression(BaseModel, Generic[T]):
    value: T

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        print(
            f"{cls.__name__}.__get_pydantic_core_schema__:",
            dict(cls=cls, source_type=source_type, handler=handler),
        )
        # return core_schema.no_info_before_validator_function(
        #     validate, handler(source_type)
        # )

        if cls.__name__ == "Expression":
            return core_schema.with_info_wrap_validator_function(
                validate_expr, handler(source_type)
            )
            # key = next(iter(input_value.keys()))
            # val = input_value[key]

        return handler(source_type)

        # return core_schema.with_info_wrap_validator_function(
        #     validate, handler(source_type)
        # )


class Happy(Expression[bool]):
    pass


d = Expression.model_validate({"$happy": True})
# d2 = MyModel(value="bob")
# d = TypeAdapter(SkipValidation[Happy]).validate_python({"value": 123})
