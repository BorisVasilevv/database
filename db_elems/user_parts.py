from db_elems.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Identity, Text
from sqlalchemy.orm import relationship


class UserPart(Base):
    __tablename__ = "UserParts"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    file_id = Column(Integer, ForeignKey("UserFiles.id"))
    part = Column(Text)
    used = Column(Boolean)

    user_file = relationship("UserFile", back_populates="user_part")
