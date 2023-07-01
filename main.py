from db_elems.database import create_db
from db_elems import user, messages, user_token, LLMs_conversation, LLMs, regeneratedMessage
import os.path

if not os.path.exists("multigpt.db"):
    create_db()
