from db_elems.database import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship


class Messages(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True)
    is_user = Column(Boolean)
    text = Column(Text)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("Users.id"))
    conversation_id = Column(Integer, ForeignKey("LLMsConversation.id"))

    user = relationship("Users", back_populates="user_message")
    llms_conversation = relationship("LLMsConversation", back_populates="message")
