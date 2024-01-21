from fastapi import APIRouter, Depends
from modules.auth.schema import schema
from modules.auth.services import auth as authService
from database.db import getDb
from sqlalchemy.ext.asyncio import AsyncSession
from ..docs import docs
from core.docs.docs import tag




dbSession = Depends(getDb)
router = APIRouter(prefix="/auth")


@router.post("/signup", tags=[tag["auth"]], response_model=schema.SignupResponseSchema, responses=docs.signupResponses)
async def signup(schema: schema.SignupSchema, session: AsyncSession = dbSession):
    return await authService.signup(schema, session)

@router.post("/login", tags=[tag["auth"]],  response_model=schema.LoginResponseSchema,  responses=docs.loginResponses)
async def login(schema: schema.LoginSchema, session: AsyncSession = dbSession):
    return await authService.login(schema, session)

@router.post("/verify-email", tags=[tag["auth"]],  response_model=schema.ResponseBaseSchema,  responses=docs.verifyEmailResponses)
async def verify_email(schema: schema.VerifyEmailSchema, session: AsyncSession = dbSession):
    return await authService.verifyEmail(schema, session)
