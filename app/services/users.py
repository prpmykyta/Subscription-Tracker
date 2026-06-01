from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import hash_password, verify_password, create_access_token
from app.repository import users as users_repo
from app.schemas import RegisterRequest, TokenResponse
from app.models.user import User


async def register_user(data: RegisterRequest, db: AsyncSession):
    existing_user = await users_repo.get_user_by_username(db, data.username)

    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    hashed_password = hash_password(data.password)
    user = User(username=data.username, hashed_password=hashed_password)

    return await users_repo.create_user(db=db, user=user)




async def authenticate_user(data: OAuth2PasswordRequestForm, db: AsyncSession) -> TokenResponse:
    user = await users_repo.get_user_by_username(db, data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token_data = {"sub": user.username}
    token = create_access_token(data=token_data)

    return TokenResponse(access_token=token, token_type="bearer")




