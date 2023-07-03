import model.model_enum
from db_elems import user, user_token, LLMs, LLMs_conversation, messages, regeneratedMessage
import os.path
from database import *
from db_elems.base import create_db

if not os.path.exists("multigpt.db"):
    create_db()



