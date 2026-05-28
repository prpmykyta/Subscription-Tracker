from app.database import engine, Base
from app.models.subscription import Subscription
from app.models.user import User

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)