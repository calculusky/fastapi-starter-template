from fastapi import APIRouter
from modules.auth.schema import schema
from modules.auth.services import auth as authService
from core.dependency import dbSession
from sqlalchemy.ext.asyncio import AsyncSession






router = APIRouter(prefix="/api/auth")


@router.post("/signup")
async def signup(schema: schema.SignupSchema, session: AsyncSession = dbSession):
    return await authService.signup(schema, session)

@router.post("/login")
async def login(schema: schema.LoginSchema):
    return await authService.login(schema)

@router.post("/verify-email")
async def login(schema: schema.VerifyEmailSchema, session: AsyncSession = dbSession):
    return await authService.verifyEmail(schema, session)

# @router.get("/users/me", response_model=schema.User)
# async def read_users_me(current_user: schema.User = Depends(authService.getCurrentUser)):
#     return current_user


# @router.get("/users/me", response_model=schema.User)
# async def read_users_me(current_user: schema.User = Depends(authService.getLoggedInUser)):
#     return current_user