from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.config import settings
from database import model

engine = create_async_engine(
    url=settings.database_url
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def syncModel():
     async with engine.begin() as conn:
            await conn.run_sync(model.Base.metadata.create_all)
            
            
async def getDb():
    db = SessionLocal()
    try:
        yield db            
    finally:
       await db.close()
            
