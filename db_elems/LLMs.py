from db_elems.base import Base
from sqlalchemy import Integer, Column, Enum, Identity
from model.model_enum import ModelEnum
from sqlalchemy.orm import relationship


class LLM(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model = Column(Enum(ModelEnum))

    user = relationship("User", back_populates="user_current_llm")



