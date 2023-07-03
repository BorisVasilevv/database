from db_elems.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Identity
from sqlalchemy.orm import relationship


class RegeneratedMessage(Base):
    __tablename__ = "RegeneratedMessage"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    og_message_id = Column(Integer, ForeignKey("Messages.id"))

    message = relationship("Message", back_populates="regenerated_message")
