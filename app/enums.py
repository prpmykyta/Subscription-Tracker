from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"