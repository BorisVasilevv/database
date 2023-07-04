import os.path
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model.database_elems import Base, UserToken, User, UserLLM, ProjectLLM, Project, FilePart, ResultData, Conversation, Message, LLM


class DBHelper:
    engine = None

    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)

    def create_db(self):
        if not os.path.exists("multigpt.db"):
            Base.create_db(self.engine)

    # def add_llm(self, model: ModelEnum):
    #     llm = LLM(model=model)
    #     with sessionmaker(self.engine) as session:
    #         session.add(llm)
    #         session.commit()
