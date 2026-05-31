from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas import CreateSubscriptionRequest, UpdateSubscriptionRequest
from app.services import subscriptions as subscriptions_service

router = APIRouter()

@router.post("/create_subscription")
async def create_subscription(data: CreateSubscriptionRequest, db: AsyncSession = Depends(get_db), current_user: User=Depends(get_current_user)):
    return await subscriptions_service.create_subscription(data=data,db=db, user_id=current_user.id)

@router.get("/subscriptions")
async def get_my_subscriptions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await subscriptions_service.get_user_subscriptions(db=db, user_id=current_user.id)

@router.patch("/subscription/{subscription_id}")
async def update_subscription(
    subscription_id: int,
    update_data: UpdateSubscriptionRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await subscriptions_service.update_subscription(db=db, subscription_id=subscription_id, user_id=current_user.id, update_data=update_data)

@router.delete("/subscription/{subscription_id}")
async def delete_subscription(subscription_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await subscriptions_service.delete_subscription(db=db, subscription_id=subscription_id, user_id=current_user.id)

@router.get("/subscriptions/statistics")
async def get_subscription_statistics(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await subscriptions_service.get_subscriptions_statistics(db=db, user_id=current_user.id)