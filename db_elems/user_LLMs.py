from db_elems.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Identity
from sqlalchemy.orm import relationship


class UserLLM(Base):
    __tablename__ = "UserLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    base_model_id = Column(Integer, ForeignKey("LLMs.id"))
    name = Column(String)

    user = relationship("User", back_populates="user_llm")
    llm_conversation = relationship("LLMsConversation", back_populates="user_llm")
    llm = relationship("LLM", back_populates="user_llm")
