from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RegisterRequest, TokenResponse, LoginRequest
from app.services import users as users_service

router = APIRouter()

@router.post("/register")
async def register_user(data: RegisterRequest, db: AsyncSession=Depends(get_db)):
    return await users_service.register_user(data=data, db=db)

@router.post("/login", response_model=TokenResponse)
async def login(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await users_service.authenticate_user(data, db=db)