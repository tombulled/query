from pydantic import BaseModel, Field


class Model(BaseModel):
    name: str = Field(kw_only=False)


m = Model("bob")
