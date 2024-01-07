from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    code: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class VerifyEmailSchema(BaseModel):
    email: EmailStr
    firstName: str | None



####

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
