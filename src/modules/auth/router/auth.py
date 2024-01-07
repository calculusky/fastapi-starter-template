from fastapi import APIRouter, Depends
from modules.auth.schema import schema
from modules.auth.services import auth as authService
from database.db import getDb
from sqlalchemy.ext.asyncio import AsyncSession


#docs
authTag = "Auth"



dbSession = Depends(getDb)
router = APIRouter(prefix="/auth")


@router.post("/signup", tags=[authTag])
async def signup(schema: schema.SignupSchema, session: AsyncSession = dbSession):
    return await authService.signup(schema, session)

@router.post("/login", tags=[authTag])
async def login(schema: schema.LoginSchema, session: AsyncSession = dbSession):
    return await authService.login(schema, session)

@router.post("/verify-email", tags=[authTag])
async def verifyEmail(schema: schema.VerifyEmailSchema, session: AsyncSession = dbSession):
    return await authService.verifyEmail(schema, session)

# @router.get("/users/me", response_model=schema.User)
# async def read_users_me(current_user: schema.User = Depends(authService.getCurrentUser)):
#     return current_user


# @router.get("/users/me", response_model=schema.User)
# async def read_users_me(current_user: schema.User = Depends(authService.getLoggedInUser)):
#     return current_user