from sqlalchemy import select
from database import model
from sqlalchemy.ext.asyncio import AsyncSession
from ..errors import errors
from fastapi import status
from core.utils import utils




async def getUserDetails(id: int, session: AsyncSession):
    stmt = select(model.User).where(model.User.id == id)
    result = await session.scalars(stmt)
    user = result.first()
    
    if not user:
        raise errors.UserNotFoundException(detail="user account not found", status_code=status.HTTP_404_NOT_FOUND)
    
    return utils.buildResponse(message="account successfully retrieved", data=user)