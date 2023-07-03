from sqlalchemy import Column, Integer, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship
from db_elems.base import Base


class UserToken(Base):
    __tablename__ = "UserToken"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    count = Column(Integer)
    last_update = Column(DateTime)

    user = relationship("User", back_populates="user_token")


