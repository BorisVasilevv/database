import enum


class ModelEnum(enum.Enum):
    GPT = "gpt"
    Bing = "Bing"


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class SubscriptionLevelEnum(enum.Enum):
    free = "standard"
    basic = "basic"
    advanced = "advanced"


class AuthorEnum(enum.Enum):
    user = "user"
    AI = "AI"
