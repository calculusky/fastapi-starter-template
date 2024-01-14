from sqlalchemy import select
from database import model
from sqlalchemy.ext.asyncio import AsyncSession
from ..errors import errors
from fastapi import status
from core.utils import utils




async def getUserDetails(id: int, session: AsyncSession):
    stmt = select(
        model.User.id, 
        model.User.identifier, 
        model.User.firstName,
        model.User.lastName, 
        model.User.email
        ).where(model.User.id == id)
    result = await session.execute(stmt)
    user = result.scalars()
    print(user)
    if not user:
        raise errors.UserNotFoundException(detail="user account not found", status_code=status.HTTP_404_NOT_FOUND)
    
    return utils.buildResponse(message="account successfully retrieved", data=user)