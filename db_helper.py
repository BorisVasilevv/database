import datetime
import os.path
import sqlalchemy
from model.enums import *
from sqlalchemy.orm import sessionmaker
from model.database_elems import Base, UserToken, User, UserLLM, ProjectLLM, \
    Project, FilePart, ResultData, SubscriptionType, Conversation, Message, LLM


class DBHelper:
    __engine = None

    def __init__(self):
        self.__engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)

    def create_db(self):
        if not os.path.exists("multigpt.db"):
            Base.create_db(self.__engine)
            with self.__create_session() as session:
                free_type = SubscriptionType(name=SubscriptionLevelEnum.free, limit=10)
                basic_type = SubscriptionType(name=SubscriptionLevelEnum.basic, limit=25)
                advanced_type = SubscriptionType(name=SubscriptionLevelEnum.advanced, limit=50)
                session.add_all([free_type, basic_type, advanced_type])
                session.commit()

    def __create_session(self):
        Session = sessionmaker(bind=self.__engine)
        return Session()

    def get_user(self, user_id: int) -> dict:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_info = user.get_simple_dict()

            subscription = session.get(SubscriptionType, user.subscription_id)
            user_info["subscription_id"] = subscription.get_simple_dict()
        return user_info

    def get_user_conversations(self, user_id: int) -> list:
        conversations = []
        with self.__create_session() as session:
            conversations_list = session.query(Conversation).filter(Conversation.user_id == user_id).all()
            for c in conversations_list:
                conversation_info = c.get_simple_dict()

                user = session.get(User, c.user_id)

                user_info = user.get_simple_dict()

                subscription = session.get(SubscriptionType, user.subscription_id)
                user_info["subscription_id"] = subscription.get_simple_dict()

                conversation_info["user_id"] = user_info

                user_llm = session.get(UserLLM, c.llm_id)
                user_llm_dict = user_llm.get_simple_dict()
                user_llm_dict["user_id"] = user.get_simple_dict()
                llm = session.get(LLM, user_llm.base_model_id)
                user_llm_dict["base_model_id"] = llm.get_simple_dict()
                conversation_info["llm_id"] = user_llm_dict

                conversations.append(conversation_info)
        return conversations

    def get_user_projects(self, user_id: int) -> list:
        projects = []
        with self.__create_session() as session:
            projects_list = session.query(Project).filter(Project.user_id == user_id).all()
            for p in projects_list:
                project_info = p.get_simple_dict()
                project_llm = session.get(ProjectLLM, p.model_id)

                project_llm_info = project_llm.get_simple_dict()

                llm = session.get(LLM, project_llm.model_id)
                project_llm_info["model_id"] = llm.get_simple_dict()

                project_info["model_id"] = project_llm_info

                projects.append(project_info)
        return projects

    def get_user_data_files(self, project_id: int) -> list:
        datas = []
        with self.__create_session() as session:
            datas_list = session.query(ResultData).filter(ResultData.project_id == project_id).all()
        for rd in datas_list:
            datas.append(rd.data)
        return datas

    def get_user_msg_history(self, conversation_id: int) -> list:
        messages_info = []
        with self.__create_session() as session:
            messages = session.query(Message).filter(Message.conversation_id == conversation_id).all()
            for message in messages:
                message_info = message.get_simple_dict()

                conversation = session.get(Conversation, message.conversation_id)
                conversation_info = conversation.get_simple_dict()

                user = session.get(User, conversation.user_id)
                user_info = user.get_simple_dict()

                subscription = session.get(SubscriptionType, user.subscription_id)
                user_info["subscription_id"] = subscription.get_simple_dict()

                conversation_info["user_id"] = user_info

                user_llm = session.get(UserLLM, conversation.llm_id)
                user_llm_dict = user_llm.get_simple_dict()
                user_llm_dict["user_id"] = user.get_simple_dict()
                llm = session.get(LLM, user_llm.base_model_id)
                user_llm_dict["base_model_id"] = llm.get_simple_dict()
                conversation_info["llm_id"] = user_llm_dict

                message["conversation_id"] = conversation_info
                messages_info.append(message_info)
        return messages_info

    def add_user(self, user_id: int, username: str):

        with self.__create_session() as session:
            free_subscription = session.query(SubscriptionType).filter(SubscriptionType.name == SubscriptionLevelEnum.free).first()
            user = User(user_id=user_id, username=username, subscription_type_id=free_subscription.id)
            session.add(user)
            session.commit()
        self.__init_user_token(user_id=user_id, limit=free_subscription.limit)

    def __init_user_token(self, user_id: int, limit: int) -> None:
        user_token = UserToken(user_id=user_id, count=limit)
        with self.__create_session() as session:
            session.add(user_token)
            session.commit()

    def add_user_model(self, user_id: int, name: str, system_name: str, base_model_id: int, prompt: str):
        with self.__create_session() as session:
            all_models_this_user = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()

            model = UserLLM(user_id=user_id, name=name, system_name=system_name, base_model_id=base_model_id,
                            prompt=prompt, is_default=all_models_this_user.len() == 0)

            session.add(model)
            session.commit()

    def add_chat(self, user_id: int, name: str, user_model_id: int) -> None:
        chat = Conversation(user_id=user_id, name=name, llm_id=user_model_id)
        with self.__create_session() as session:
            session.add(chat)
            session.commit()

    def add_message(self, convo_id: int, question: str, answer: str) -> None:
        message = Message(conversation_id=convo_id, question=question, answer=answer)
        with self.__create_session() as session:
            session.add(message)
            session.commit()

    def add_project(self, user_id: int, name: str, mimetype: str, file: bytes) -> None:
        project = Project(user_id=user_id, name=name, mimetype=mimetype, file=file)
        with self.__create_session() as session:
            session.add(project)
            session.commit()

    def update_default_model(self, user_id: int, user_model_id: int) -> None:
        with self.__create_session() as session:
            user_llms = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()

            if user_llms is not None and any(model.id == user_model_id for model in user_llms):
                for model in user_llms:
                    model.is_default = False
                    if model.id == user_model_id:
                        model.is_default = True
                session.commit()

    def update_plan(self, user_id: int, plan: SubscriptionLevelEnum) -> None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == plan).first()
            if user is not None and subscription is not None:
                user.subscription_id = subscription.id
                session.commit()

    def update_limits(self, plan: SubscriptionLevelEnum, new_limit: int) -> None:
        with self.__create_session() as session:
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == plan).first()
            if subscription is not None:
                subscription.limit = new_limit
                session.commit()
