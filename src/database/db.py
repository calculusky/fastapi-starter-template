from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import config
from database import model

engine = create_async_engine(
    url=config.databaseUrl
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def syncModel():
     async with engine.begin() as conn:
            await conn.run_sync(model.Base.metadata.drop_all)
            await conn.run_sync(model.Base.metadata.create_all)
            
            
async def getDb():
    db = SessionLocal()
    try:
        yield db            
    finally:
       await db.close()
            
