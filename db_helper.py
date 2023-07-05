import datetime
import os.path
import sqlalchemy
from model.enums import *
from sqlalchemy.orm import sessionmaker
from model.database_elems import Base, UserToken, User, UserLLM, ProjectLLM, Project, FilePart, ResultData, Conversation, Message, LLM


class DBHelper:
    __engine = None

    def __init__(self):
        self.__engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)

    def create_db(self):
        if not os.path.exists("multigpt.db"):
            Base.create_db(self.__engine)

    def __create_session(self):
        return sessionmaker(bind=self.__engine)

    def get_user(self, user_id: int) -> dict:
        with self.__create_session() as session:
            user = session.get(User, user_id)
        return user.get_info()

    def get_user_conversation(self, user_id: int) -> list:
        conversations = []
        with self.__create_session() as session:
            conversations_list = session.query(Conversation).filter(Conversation.user_id is user_id)
        for c in conversations_list:
            conversations.append(c.get_info())
        return conversations

    def get_user_projects(self, user_id: int) -> list:
        projects = []
        with self.__create_session() as session:
            projects_list = session.query(Project).filter(Project.user_id is user_id)
        for p in projects_list:
            projects.append(p.get_info())
        return projects

    def get_user_data_files(self, project_id: int) -> list:
        datas = []
        with self.__create_session() as session:
            datas_list = session.query(ResultData).filter(ResultData.project_id is project_id)
        for rd in datas_list:
            datas.append(rd.data)
        return datas

    def get_user_msg_history(self, conversation_id: int) -> list:
        messages_info = []
        with self.__create_session() as session:
            messages = session.query(Message).filter(Message.conversation_id is conversation_id)
        for rd in messages:
            messages_info.append(rd.data)
        return messages_info

    def add_user(self, user_id: int, username: str):
        pass
        # new_user = User(id=user_id, username=username, registration_date=datetime.datetime.now(),
        #                 subscription=SubscriptionLevelEnum.free, default_model_id=None)
        # with self.__create_session() as session:
        #     session.add(new_user)
        #     session.commit()

    def add_user_model(self, user_id: int, name: str, system_name: str, base_model_id: int, prompt: str):
        pass