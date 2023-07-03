from model import model_enum, subscribe_level_enum, role_enum
from sqlalchemy.orm import sessionmaker
from db_elems import LLMs, LLMs_conversation, base, messages, regeneratedMessage, user, user_token
import datetime


def add_llm(model: model_enum.ModelEnum):
    llm = LLMs.LLM(model=model)
    with sessionmaker(base.engine) as session:
        session.add(llm)
        session.commit()


def add_llm_conversation(conversation_id: str, llm_model: str):
    llm_conversation = LLMs_conversation.LLMsConversation(conversation_id=conversation_id, llm_model=llm_model)
    with sessionmaker(base.engine) as session:
        session.add(llm_conversation)
        session.commit()


def add_message(is_user: bool, text: str, time: datetime, user_id: int, llm_conversation_id: int):
    if time is None:
        time = datetime.datetime.now()

    message = messages.Message(is_user=is_user, text=text, time=time, user_id=user_id,
                               llm_conversation_id=llm_conversation_id)

    with sessionmaker(base.engine) as session:
        session.add(message)
        session.commit()


def add_regenerated_message(og_message_id: int):
    reg_message = regeneratedMessage.RegeneratedMessage(og_message_id=og_message_id)

    with sessionmaker(base.engine) as session:
        session.add(reg_message)
        session.commit()


def add_user(username: str, registration_date: datetime,
             subscribe_level: subscribe_level_enum.SubscribeLevelEnum, role: role_enum.RoleEnum, current_llm: int):

    new_user = user.User(username=username, registration_date=registration_date,
                         subscribe_level=subscribe_level, role=role, current_llm=current_llm)
    with sessionmaker(base.engine) as session:
        session.add(new_user)
        session.commit()


def add_user_token(user_id: int, count: int, last_update: datetime):
    if last_update is None:
        last_update = datetime.datetime.now()

    tokens = user_token.UserToken(user_id=user_id, count=count,last_update=last_update)

    with sessionmaker(base.engine) as session:
        session.add(tokens)
        session.commit()
        