from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Date, Boolean, ForeignKey, Enum

from app.database import Base
from app.enums import SubscriptionTypeEnum

if TYPE_CHECKING:
    from app.models.user import User

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    type: Mapped[SubscriptionTypeEnum] = mapped_column(Enum(SubscriptionTypeEnum))

    start_date: Mapped[date] = mapped_column(Date)
    next_payment_date: Mapped[date] = mapped_column(Date)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")