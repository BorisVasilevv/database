import datetime

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
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

    def get_info(self):
        result = {
            "id": self.id,
            "count": self.count,
            "last_update": self.last_update
        }

        with sessionmaker(bind=engine) as session:
            user = session.get(User, self.id)

        if user is not None:
            result["user_id"] = user.get_info()
        else:
            result["user_id"] = None
        return result


class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    model_id = Column(Integer, ForeignKey("ProjectLLMs.id"))
    name = Column(String)
    mimetype = Column(String)
    file = Column(BLOB)

    user = relationship("User", back_populates="project")
    file_part = relationship("FilePart", back_populates="project")
    result_data = relationship("ResultData", back_populates="project")
    project_llm = relationship("ProjectLLM", back_populates="project")

    def get_info(self):
        result = {
            "id": self.id,
            "name": self.name,
            "mimetype": self.mimetype,
            "file": self.file
        }

        with sessionmaker(bind=engine) as session:
            user = session.get(User, self.user_id)
            pr_llm = session.get(ProjectLLM, self.model_id)
        if user is not None:
            result["user_id"] = user.get_info()
        if pr_llm is not None:
            result["model_id"] = pr_llm.get_info()

        return result


class FilePart(Base):
    __tablename__ = "FileParts"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.id"))
    part = Column(Text)
    used = Column(Boolean)

    project = relationship("Project", back_populates="file_part")

    def get_info(self):
        result = {
            "id": self.id,
            "part": self.part,
            "used": self.used
        }

        with sessionmaker(bind=engine) as session:
            project = session.get(Project, self.project_id)
        if project is not None:
            result["project_id"] = project.get_info()

        return result


class ResultData(Base):
    __tablename__ = "ResultData"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(ForeignKey("Projects.id"))
    data = Column(Text)

    project = relationship("Project", back_populates="result_data")

    def get_info(self):
        result = {
            "id": self.id,
            "data": self.data
        }

        with sessionmaker(bind=engine) as session:
            project = session.get(Project, self.project_id)
        if project is not None:
            result["project_id"] = project.get_info()

        return result


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

    def get_info(self):
        result = {
            "id": self.id,
            "username": self.username,
            "registration_date": self.registration_date,
            "subscription": self.subscription,
        }

        with sessionmaker(bind=engine) as session:
            user_llm = session.get(UserLLM, self.default_model_id)

        if user_llm is not None:
            user_llm_dict = {
                "id": user_llm.id,
                "user_id": user_llm.user_id,
                "name": user_llm.name,
                "system_name": user_llm.system_name,
                "prompt": user_llm.prompt
            }

            with sessionmaker(bind=engine) as session:
                llm = session.get(LLM, user_llm.base_model_id)
            if llm is not None:
                user_llm_dict["base_model_id"] = llm.get_info()

            result["default_model_id"] = user_llm_dict

        return result


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

    def get_info(self):
        result = {
            "id": self.id,
            "name": self.name,
            "system_name": self.system_name,
            "prompt": self.prompt
        }

        with sessionmaker(bind=engine) as session:
            user_llm = session.get(User, self.user_id)
            llm = session.get(LLM, user_llm.base_model_id)

        if user_llm is not None:
            result["user_id"] = user_llm.get_info()
        if llm is not None:
            result["base_model_id"] = llm.get_info()

        return result


class ProjectLLM(Base):
    __tablename__ = "ProjectLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model_id = Column(Integer, ForeignKey("LLMs.id"))
    system_name = Column(String)
    prompt = Column(Text)

    project = relationship("Project", back_populates="project_llm")
    llm = relationship("LLM", back_populates="project_llm")

    def get_info(self):
        result = {
            "id": self.id,
            "system_name": self.system_name,
            "prompt": self.prompt
        }

        with sessionmaker(bind=engine) as session:
            llm = session.get(LLM, self.model_id)
        if llm is not None:
            result["model_id"] = llm.get_info()

        return result


class Conversation(Base):
    __tablename__ = "Conversations"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    name = Column(String)
    llm_id = Column(Integer, ForeignKey("UserLLMs.id"))

    user = relationship("User", back_populates="conversation")
    user_llm = relationship("UserLLM", back_populates="conversation")
    message = relationship("Message", back_populates="conversation")

    def get_info(self):
        result = {
            "id": self.id,
            "name": self.name
        }

        with sessionmaker(bind=engine) as session:
            user = session.get(User, self.user_id)
            user_llm = session.get(UserLLM, self.llm_id)

        if user is not None:
            result["user_id"] = user.get_info()
        if user_llm is not None:
            result["llm_id"] = user_llm.get_info()

        return result


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    author = Column(Enum(AuthorEnum))
    text = Column(Text)
    time = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey("Conversations.id"))

    conversation = relationship("Conversation", back_populates="message")

    def get_info(self):
        result = {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "time": self.time
        }

        with sessionmaker(bind=engine) as session:
            conversation = session.get(Conversation, self.conversation_id)
        if conversation is not None:
            result["conversation_id"] = conversation.get_info()


class LLM(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model = Column(Enum(ModelEnum))

    user_llm = relationship("UserLLM", back_populates="llm")
    project_llm = relationship("ProjectLLM", back_populates="llm")

    def get_info(self):
        result = {
            "id": self.id,
            "model": self.model
        }
        return result
