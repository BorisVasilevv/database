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
            user_info["subscription"] = user.subscription_type.get_simple_dict()
            user_info["token"] = user.user_token[0].get_simple_dict()

            all_llms = user.user_llm
            for llm in all_llms:
                if llm.is_default:
                    default_llm = llm
                    break
            if default_llm is None:
                user_info["default_model"] = None
            else:
                user_info["default_model"] = default_llm.get_simple_dict()
        return user_info

    def get_user_conversations(self, user_id: int) -> list[dict]:
        conversations = []
        with self.__create_session() as session:
            conversations_list = session.query(Conversation).filter(Conversation.user_id == user_id).all()
            for c in conversations_list:
                conversation_info = c.get_simple_dict()
                conversation_info["user_id"] = c.user_id
                user_llm = c.user_llm
                conversation_info["llm"] = user_llm.get_simple_dict()
                conversation_info["llm"]["system_name"] = user_llm.system_name
                conversations.append(conversation_info)
        return conversations

    # Не тестил
    def get_user_models(self, user_id: int, offset: int, limit: int) -> list[dict]:
        models_info = []
        try:
            with self.__create_session() as session:
                user_llms = session.query(UserLLM).filter(UserLLM.user_id == user_id).offset(offset).limit(limit).all()
                for model in user_llms:
                    model_info = model.get_full_dict()
                    model_info["model"] = model.llm.get_simple_dict()
                    models_info.append(model_info)
            return models_info
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return models_info

    # Не тестил
    def get_user_projects(self, user_id: int, offset: int, limit: int) -> list[dict]:
        projects = []
        try:
            with self.__create_session() as session:
                projects_list = session.query(Project).filter(Project.user_id == user_id).offset(offset).limit(limit).all()
                for p in projects_list:
                    project_info = p.get_simple_dict()
                    project_info["model"] = p.project_llm.get_simple_dict()
                    project_info["model"]["system_name"] = p.name
                    projects.append(project_info)
            return projects
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return projects

    # Не тестил
    def get_user_data_files(self, project_id: int) -> list:
        datas = []
        with self.__create_session() as session:
            datas_list = session.query(ResultData).filter(ResultData.project_id == project_id).all()
        for rd in datas_list:
            datas.append(rd.data)
        return datas

    # Не тестил
    def get_user_msg_history(self, conversation_id: int, limit: int, offset: int) -> list[dict]:
        messages_info = []
        try:
            with self.__create_session() as session:
                messages = session.query(Message).filter(Message.conversation_id == conversation_id)\
                    .offset(offset).limit(limit).all()
                for message in messages:
                    message_info = message.get_simple_dict()
                    message_info["conversation"] = message.conversation.get_simple_dict()
                    messages_info.append(message_info)
        except sqlalchemy.orm.exc.NoResultFound:
            return []
        finally:
            return messages_info

    # Не тестил
    def get_project_count(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            projects_list = session.query(Project).filter(Project.user_id == user_id).all()
            result = projects_list.__len__()
        return result

    # Не тестил
    def get_message_count(self, convo_id: int) -> int:
        result: int
        with self.__create_session() as session:
            messages = session.query(Message).filter(Message.conversation_id == convo_id).all()
            result = messages.__len__()
        return result

    # Не тестил
    def get_model_count(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            user_llm_list = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()
            result = user_llm_list.__len__()
        return result

    # Не тестил
    def get_count_conversation(self, user_id: int) -> int:
        result: int
        with self.__create_session() as session:
            conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
            result = conversations.__len__()
        return result

    def add_user(self, user_id: int, username: str):
        limit: int
        with self.__create_session() as session:
            free_subscription = session.query(SubscriptionType)\
                .filter(SubscriptionType.name == SubscriptionLevelEnum.free).first()

            user = User(user_id=user_id, username=username, subscription_type_id=free_subscription.id)
            session.add(user)
            limit = free_subscription.limit
            session.commit()
        self.__init_user_token(user_id=user_id, limit=limit)

    def __init_user_token(self, user_id: int, limit: int) -> None:
        user_token = UserToken(user_id=user_id, count=limit)
        with self.__create_session() as session:
            session.add(user_token)
            session.commit()

    def add_user_model(self, user_id: int, name: str, system_name: str, base_model_id: int, prompt: str):
        with self.__create_session() as session:
            all_models_this_user = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()

            model = UserLLM(user_id=user_id, name=name, system_name=system_name, base_model_id=base_model_id,
                            prompt=prompt, is_default=all_models_this_user.__len__() == 0)

            session.add(model)
            session.commit()

    # Не тестил
    def add_chat(self, user_id: int, name: str, user_model_id: int) -> None:
        chat = Conversation(user_id=user_id, name=name, llm_id=user_model_id)
        with self.__create_session() as session:
            session.add(chat)
            session.commit()

    # Не тестил
    def add_message(self, convo_id: int, question: str, answer: str) -> None:
        message = Message(conversation_id=convo_id, question=question, answer=answer)
        with self.__create_session() as session:
            session.add(message)
            session.commit()

    # Не тестил
    def add_project(self, user_id: int, name: str, mimetype: str, file: bytes) -> None:
        project = Project(user_id=user_id, name=name, mimetype=mimetype, file=file)
        with self.__create_session() as session:
            session.add(project)
            session.commit()

    # Не тестил
    def update_default_model(self, user_id: int, user_model_id: int) -> None:
        with self.__create_session() as session:
            user_llms = session.query(UserLLM).filter(UserLLM.user_id == user_id).all()

            if user_llms is not None and any(model.id == user_model_id for model in user_llms):
                for model in user_llms:
                    model.is_default = False
                    if model.id == user_model_id:
                        model.is_default = True
                session.commit()

    # Не тестил
    def update_plan(self, user_id: int, plan: SubscriptionLevelEnum) -> None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == plan).first()
            if user is not None and subscription is not None:
                user.subscription_id = subscription.id
                session.commit()

    # Не тестил
    def update_limits(self, plan: SubscriptionLevelEnum, new_limit: int) -> None:
        with self.__create_session() as session:
            subscription = session.query(SubscriptionType).filter(SubscriptionType.name == plan).first()
            if subscription is not None:
                subscription.limit = new_limit
                session.commit()

    # Не тестил
    # смотрит на last_update, если оно
    # не сегодня добавляет количество токенов, в зависимости от подписки,
    # после этого смотрит сколько токенов, если не 0 вернёт True
    def can_user_ask_question(self, user_id: int) -> bool:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_token = user.user_token[0]
            if user_token.last_update.day != datetime.datetime.now().date().day:
                subscription = user.subscription_type
                user_token.count = subscription.limit
                session.commit()
                return True
            else:
                return user_token.count > 0

    # Не тестил
    def user_ask(self, user_id: int) -> None:
        with self.__create_session() as session:
            user = session.get(User, user_id)
            user_token = user.user_token[0]
            user_token.count -= 1
            session.commit()

