import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Identity, ForeignKey, DateTime, String, Text, Boolean, Enum, BLOB
from model.enums import *


engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)


class Base(DeclarativeBase):
    @classmethod
    def create_db(cls, some_engine):
        cls.metadata.create_all(bind=some_engine)


class UserToken(Base):
    __tablename__ = "UserToken"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    count = Column(Integer)
    last_update = Column(DateTime)

    user = relationship("User", back_populates="user_token")


class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    model_id = Column(Integer, ForeignKey("ProjectLLMs.id"))
    name = Column(String)
    mimetype = Column(String)
    file = Column(BLOB)

    user = relationship("User", back_populates="project")
    file_part = relationship("UserPart", back_populates="project")
    result_data = relationship("ResultData", back_populates="project")
    project_llm = relationship("ProjectLLM", back_populates="project")


class FilePart(Base):
    __tablename__ = "FileParts"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.id"))
    part = Column(Text)
    used = Column(Boolean)

    project = relationship("Project", back_populates="file_part")


class ResultData(Base):
    __tablename__ = "ResultData"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(ForeignKey("Projects.id"))
    data = Column(Text)

    project = relationship("Project", back_populates="result_data")


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    registration_date = Column(DateTime)
    subscription = Column(Enum(SubscriptionLevelEnum))
    default_model_id = Column(Integer, ForeignKey("UserLLMs.id"))

    user_token = relationship("UserToken", back_populates="user")
    project = relationship("Project", back_populates="user")
    user_llm = relationship("UserLLM", back_populates="user")
    conversation = relationship("Conversation", back_populates="user")


class UserLLM(Base):
    __tablename__ = "UserLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    base_model_id = Column(Integer, ForeignKey("LLMs.id"))
    name = Column(String)
    system_name = Column(String)
    prompt = Column(Text)

    user = relationship("User", back_populates="user_llm")
    conversation = relationship("Conversation", back_populates="user_llm")
    llm = relationship("LLM", back_populates="user_llm")


class ProjectLLM(Base):
    __tablename__ = "ProjectLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model_id = Column(Integer, ForeignKey("LLMs.id"))
    system_name = Column(String)
    prompt = Column(Text)

    project = relationship("Project", back_populates="project_llm")
    llm = relationship("LLM", back_populates="project_llm")


class Conversation(Base):
    __tablename__ = "Conversations"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    name = Column(String)
    llm_id = Column(Integer, ForeignKey("UserLLMs.id"))

    user = relationship("User", back_populates="conversation")
    user_llm = relationship("UserLLM", back_populates="conversation")
    message = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    author = Column(Enum(AuthorEnum))
    text = Column(Text)
    time = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey("Conversations.id"))

    conversation = relationship("Conversation", back_populates="message")


class LLM(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model = Column(Enum(ModelEnum))

    user_llm = relationship("UserLLM", back_populates="llm")
    project_llm = relationship("LLM", back_populates="llm")

