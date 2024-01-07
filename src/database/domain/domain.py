# from .base import Base
# from typing import Generic, TypeVar
# from database import model
# from pydantic import BaseModel
# from sqlalchemy import select

# TModel = TypeVar("TModel", model.User, model.Post)

# class Domain(Generic[TModel], Base):
#     def __init__(self, Model: TModel) -> None:
#         super().__init__()
#         self.Model = Model

    
#     async def create(self, body: BaseModel) -> TModel:
#         async with self.asyncSession() as session:
#             data = self.Model(**body.model_dump())
#             session.add(data)
#             await session.commit()
#             await session.refresh(data)
#             return data
        
#     async def findOne(self, query):
        
#         model.User().metadata
#         async with self.asyncSession() as session:
#             stmt = select(model.User).where(model.User["email"] == "user@example.com")
#             result = await session.execute(stmt)
#             return result.scalars().first()
        

