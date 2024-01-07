from fastapi import APIRouter
from modules.auth.schema import schema
from modules.auth.services import auth as authService
from sqlalchemy.ext.asyncio import AsyncSession
from modules.auth.services import auth as authService
from fastapi import Depends
from database import model


#docs
userTag = "User"



authUserGuard = Depends(authService.authGuard)

router = APIRouter(prefix="/user")

@router.get("/details", tags=[userTag])
async def userDetails(user: model.User = authUserGuard):
    return user