from db_elems.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class RegeneratedMessage(Base):
    __tablename__ = "RegeneratedMessage"
    id = Column(Integer, primary_key=True)
    og_message_id = Column(Integer, ForeignKey("Messages.id"))

    message = relationship("Messages", back_populates="regenerated_message")
