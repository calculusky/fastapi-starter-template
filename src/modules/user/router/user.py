from fastapi import APIRouter
from ..schema import schema
from modules.auth.services import auth as authService
from fastapi import Depends
from database import model
from ..services import user as userService
from ..docs import docs
from core.docs.docs import tag
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import getDb







authUserGuard = Depends(authService.authGuard)
dbSession = Depends(getDb)

router = APIRouter(prefix="/user")

@router.get("/details", tags=[tag["user"]], response_model=schema.UserDetailResponseSchema, responses=docs.userDetailsResponses)
async def user_details(user: model.User = authUserGuard, session: AsyncSession = dbSession):
    return await userService.getUserDetails(user.id, session)