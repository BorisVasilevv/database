from db_elems.base import Base
from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey, Identity
from sqlalchemy.orm import relationship
import datetime


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    author = Column(String)
    text = Column(Text)
    time = Column(DateTime)
    llm_conversation_id = Column(Integer, ForeignKey("LLMsConversation.id"))

    llm_conversation = relationship("LLMsConversation", back_populates="message")
