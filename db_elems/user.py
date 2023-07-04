from db_elems.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Identity
from model.enums import RoleEnum, SubscriptionLevelEnum
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    username = Column(String)
    registration_date = Column(DateTime)
    subscription = Column(Enum(SubscriptionLevelEnum))
    default_model_id = Column(Integer, ForeignKey("UserLLMs.id"))

    user_token = relationship("UserToken", back_populates="user")
    user_file = relationship("UserFile", back_populates="user")
    user_llm = relationship("UserLLM", back_populates="user")
    llm_conversation = relationship("LLMsConversation", back_populates="user")
