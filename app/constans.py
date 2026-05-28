from app.enums import SubscriptionTypeEnum

SUBSCRIPTION_TYPE_DAYS = {
    SubscriptionTypeEnum.weekly: 7,
    SubscriptionTypeEnum.monthly: 30,
    SubscriptionTypeEnum.yearly: 365,
}