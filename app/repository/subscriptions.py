from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription
from sqlalchemy import select, delete


async def get_subscription_by_name(db: AsyncSession, name: str, user_id: int):
    query = select(Subscription).where(Subscription.name == name, Subscription.user_id == user_id)
    result = await db.execute(query)

    return result.scalar_one_or_none()

async def create_subscription(db: AsyncSession, subscription: Subscription):
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription

async def get_user_subscriptions(db: AsyncSession, user_id: int):
    query = select(Subscription).where(Subscription.user_id == user_id)
    result = await db.execute(query)

    return list(result.scalars().all())

async def get_subscription_by_id(db: AsyncSession, subscription_id: int, user_id: int):
    query = select(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == user_id)
    result = await db.execute(query)

    return result.scalar_one_or_none()

async def check_name_exists_for_other_subscription(db: AsyncSession, name: str, user_id: int, current_subscription_id: int):
    query = select(Subscription).where(
        Subscription.name == name,
        Subscription.user_id == user_id,
        Subscription.id != current_subscription_id
    )
    result = await db.execute(query)

    return result.scalars().first() is not None

async def delete_subscription(db: AsyncSession, subscription_id: int, user_id: int):
    query = delete(Subscription).where(Subscription.id == subscription_id, Subscription.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0