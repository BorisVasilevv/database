from db_elems.base import Base
from sqlalchemy import Integer, Column, Enum, Identity
from model.enums import ModelEnum
from sqlalchemy.orm import relationship


class LLM(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model = Column(Enum(ModelEnum))

    user_llm = relationship("UserLLM", back_populates="llm")



