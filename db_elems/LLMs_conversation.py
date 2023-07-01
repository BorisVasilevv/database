from db_elems.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class LLMsConversation(Base):
    __tablename__ = "LLMsConversation"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String)
    llm_model = Column(String)
    message = relationship("Messages", back_populates="llms_conversation")
