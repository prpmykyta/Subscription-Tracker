from datetime import date, timedelta
from pydantic import BaseModel, Field, field_validator
from app.enums import SubscriptionTypeEnum


class CreateSubscriptionRequest(BaseModel):
    name: str = Field(..., max_length=100)
    price: float = Field(...)
    subscription_type: SubscriptionTypeEnum
    start_date: date
    is_active: bool = True

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Subscription name cannot be empty")
        return v
    @field_validator('price')
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price cannot be negative")
        return v

class UpdateSubscriptionRequest(BaseModel):
    name: str = Field(None, max_length=100)
    price: float = Field(None)
    subscription_type: SubscriptionTypeEnum = None
    start_date: date = None
    is_active: bool = None

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str