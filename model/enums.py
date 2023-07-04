import enum


class ModelEnum(enum.Enum):
    GPT = "gpt"
    Bing = "Bing"


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class SubscriptionLevelEnum(enum.Enum):
    free = "standard"
    advanced = "advanced"
    max = "max"


class AuthorEnum(enum.Enum):
    user = "user"
    AI = "AI"
