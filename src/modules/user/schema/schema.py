from pydantic import BaseModel
from core.schema.schema import ResponseBaseSchema


class UserResponseData(BaseModel):
    id: int
    identifier: str
    firstName: str
    lastName: str
    email: str


class UserDetailResponseSchema(ResponseBaseSchema):
   data: UserResponseData
