from db_elems import LLMs, LLMs_conversation, messages, result_data, user, user_files, user_LLMs, user_parts, user_token
import os.path
from db_elems.base import create_db

if not os.path.exists("multigpt.db"):
    create_db()



