from db_elems.base import Base
from sqlalchemy import Column, Integer, String, Identity, ForeignKey
from sqlalchemy.orm import relationship


class LLMsConversation(Base):
    __tablename__ = "LLMsConversation"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    llm_id = Column(Integer, ForeignKey("UserLLMs.id"))
    name = Column(String)

    user = relationship("User", back_populates="llm_conversation")
    user_llm = relationship("UserLLM", back_populates="llm_conversation")
    message = relationship("Message", back_populates="llm_conversation")
