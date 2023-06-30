from db_elems.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from model.role_enum import RoleEnum
from model.subscribe_level_enum import SubscribeLevelEnum
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    registration_date = Column(DateTime)
    subscribe_level = Column(Enum(SubscribeLevelEnum))
    role = Column(Enum(RoleEnum))

    user_token = relationship("UserToken", back_populates="user")
    user_message = relationship("Messages", back_populates="user")
