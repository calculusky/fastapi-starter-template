from pydantic import BaseModel, EmailStr, Field
from core.schema.schema import ResponseBaseSchema


class SignupSchema(BaseModel):
    firstName: str = Field(..., example="John")
    lastName: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., example="pass1234")
    code: str = Field(..., example="25673")
    

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., example="pass1234")
    
class VerifyEmailSchema(BaseModel):
    email: EmailStr  = Field(..., example="johndoe@example.com")
    firstName: str | None = Field(default=None, example="John")
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    identifier: str | None = None


class CreateUser(BaseModel):
    email: str
    firstName: str
    lastName: str
    password: str
    identifier: str

class AccountVerificationRequestSchema(BaseModel):
    email: str
    code: str
    

    
class SignupResponseData(BaseModel):
    accessToken: str
    tokenType: str = "bearer"

class SignupResponseSchema(ResponseBaseSchema):
    data: SignupResponseData
    
class LoginResponseSchema(SignupResponseSchema):
   pass

    