import enum


class ModelEnum(enum.Enum):
    ChatGPT = "chinchilla"
    Claude = "a2"


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

class TestEnum(enum.Enum):
    pass


class SubscriptionLevelEnum(enum.Enum):
    free = "free"
    basic = "basic"
    advanced = "advanced"
