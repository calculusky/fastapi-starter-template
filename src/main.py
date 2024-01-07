from src.www.app import initApp
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.syncModel()
    yield

app = FastAPI(lifespan=lifespan)
def bootstrap():
    initApp(app)

bootstrap()


