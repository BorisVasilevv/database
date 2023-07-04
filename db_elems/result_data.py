from db_elems.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Identity, Text
from sqlalchemy.orm import relationship


class ResultData(Base):
    __tablename__ = "ResultData"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    file_id = Column(ForeignKey("UserFiles.id"))
    data = Column(Text)

    user_file = relationship("UserFile", back_populates="result_data")
