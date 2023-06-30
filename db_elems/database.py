import sqlalchemy
from sqlalchemy.orm import DeclarativeBase

engine = sqlalchemy.create_engine('sqlite:///multigpt.db')


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(bind=engine)
