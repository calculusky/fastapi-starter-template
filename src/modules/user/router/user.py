from fastapi import APIRouter
from ..schema import schema
from modules.auth.services import auth as authService
from fastapi import Depends
from database import model
from ..services import user as userService
from ..docs import docs
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import getDb



#docs
userTag = "User"



authUserGuard = Depends(authService.authGuard)
dbSession = Depends(getDb)
# response_model=schema.UserDetailResponseSchema,

router = APIRouter(prefix="/user")

@router.get("/details", tags=[userTag],  responses=docs.userDetailsResponses)
async def userDetails(user: model.User = authUserGuard, session: AsyncSession = dbSession):
    return await userService.getUserDetails(user.id, session)