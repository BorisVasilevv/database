from db_elems.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Identity
from sqlalchemy.orm import relationship


class UserFile(Base):
    __tablename__ = "UserFiles"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    name = Column(String)
    mimetype = Column(String)

    user = relationship("User", back_populates="user_file")
    user_part = relationship("UserPart", back_populates="user_file")
    result_data = relationship("ResultData", back_populates="user_file")
