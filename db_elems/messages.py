from db_elems.base import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, ForeignKey, Identity
from sqlalchemy.orm import relationship
import datetime


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    is_user = Column(Boolean)
    text = Column(Text)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("Users.id"))
    llm_conversation_id = Column(Integer, ForeignKey("LLMsConversation.id"))

    user = relationship("User", back_populates="user_message")
    llms_conversation = relationship("LLMsConversation", back_populates="message")
    regenerated_message = relationship("RegeneratedMessage", back_populates="message")



