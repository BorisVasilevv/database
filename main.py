import datetime
from model.enums import *
from db_helper import DBHelper

db_helper = DBHelper()
db_helper.create_db()
db_helper.add_user(1, "vrvrv")
print(db_helper.get_user(1))
# print(db_helper.get_new_user_count(datetime.datetime(2000, 2, 11), datetime.datetime.now()))
#
#
#     if db_helper.can_user_ask_question(9):
#         db_helper.add_message(1, "dfbtdb", "rbtbgf")
#
#
# amount = db_helper.get_message_count(1)
# c = 0
# while c < amount:
#     print(db_helper.get_user_msg_history(1, c, 2))
#     print("\n\n\n")
#     c += 2
