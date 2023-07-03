from db_elems.base import Base
from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship


class LLMsConversation(Base):
    __tablename__ = "LLMsConversation"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    conversation_id = Column(String)
    llm_model = Column(String)
    message = relationship("Message", back_populates="llms_conversation")
