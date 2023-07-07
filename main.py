from db_helper import DBHelper
from model.database_elems import User, UserToken


db_helper = DBHelper()

db_helper.create_db()
# db_helper.add_user(9, "test")

u = db_helper.get_user(9)
i = db_helper.get_user_conversations(9)
y = 7

