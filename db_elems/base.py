import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from model.model_enum import ModelEnum


engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(bind=engine)




