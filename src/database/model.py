from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, String, func, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

metadata = MetaData()

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstName: Mapped[str] = mapped_column(String(50))
    lastName: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    identifier: Mapped[str] = mapped_column(String(50), unique=True)
    password:  Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
   


class Post(Base):
    __tablename__ = "Posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class AccountVerificationRequest(Base):
    __tablename__ = "AccountVerificationRequests"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())