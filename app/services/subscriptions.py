from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription
from app.schemas import CreateSubscriptionRequest, UpdateSubscriptionRequest
from app.repository import subscriptions as subscription_repo
from app.constans import SUBSCRIPTION_TYPE_DAYS

async def create_subscription(data: CreateSubscriptionRequest, db: AsyncSession, user_id: int):
    existing_subscription = await subscription_repo.get_subscription_by_name(db, data.name, user_id)
    if existing_subscription:
        raise HTTPException(status_code=400, detail=f"Subscription {data.name} already exists")

    days = SUBSCRIPTION_TYPE_DAYS[data.type]
    next_payment_date = data.start_date + timedelta(days=days)

    subscription = Subscription(
        name=data.name,
        price=data.price,
        type=data.type,
        start_date=data.start_date,
        next_payment_date=next_payment_date,
        is_active=True,
        user_id=user_id
    )

    return await subscription_repo.create_subscription(db, subscription)

async def get_user_subscriptions(db: AsyncSession, user_id: int):
    return await subscription_repo.get_user_subscriptions(db, user_id)

async def update_subscription(db: AsyncSession, subscription_id, user_id, update_data: UpdateSubscriptionRequest):
    subscription = await subscription_repo.get_subscription_by_id(db, subscription_id, user_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    data_dict = update_data.model_dump(exclude_unset=True)

    if "name" in data_dict:
        new_name = data_dict["name"]
        name_is_taken = await subscription_repo.check_name_exists_for_other_subscription(db,
                                                                                         name=new_name,
                                                                                         user_id=user_id,
                                                                                         current_subscription_id=subscription_id
                                                                                         )
        if name_is_taken:
            raise HTTPException(status_code=400, detail=f"You already have another subscription with the name {new_name}")

    for key, value in data_dict.items():
        setattr(subscription, key, value)

    if "start_date" in data_dict or "type" in data_dict:
        current_start_date = subscription.start_date
        current_type = subscription.type

        subscription.next_payment_date = current_start_date + timedelta(days=SUBSCRIPTION_TYPE_DAYS[current_type])

    await db.commit()
    await db.refresh(subscription)
    return subscription

async def delete_subscription(db: AsyncSession, subscription_id: int, user_id: int):
    success = await subscription_repo.delete_subscription(db, subscription_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return {"detail": "Subscription deleted successfully"}














