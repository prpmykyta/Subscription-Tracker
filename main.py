from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.users import router as users_router
from app.api.v1.subscriptions import router as subscriptions_router

from app.database import engine
from app.create_tables import create_tables



@asynccontextmanager
async def lifespan(app):
    await create_tables()
    yield
app = FastAPI(lifespan=lifespan)


app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(subscriptions_router, prefix="/api/v1", tags=["subscriptions"])