from db_elems.database import Base
from sqlalchemy import Integer, Column, Enum, Identity
from model.model_enum import ModelEnum
from sqlalchemy.orm import relationship


class LLMs(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, primary_key=True)
    model = Column(Enum(ModelEnum))

    user = relationship("Users", back_populates="user_current_llm")
