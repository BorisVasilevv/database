import datetime
from model.enums import *
from db_helper import DBHelper

db_helper = DBHelper()
db_helper.create_db()
file = open("r.txt", "rb")
# print(db_helper.get_project_count(1))
print(db_helper.get_project_name(1))
# print(db_helper.get_user_projects(1, 0, 20))



# db_helper.add_project(1,"crecerc","cwcre",1, None, file.read(),"evrtvrt")

# a = ModelEnum.Claude
# db_helper.add_project(1, "vgrev00,0,","vvfs",1,"vrvr", file.read(), "esgrs")
# db_helper.update_limits(SubscriptionLevelEnum.free.value, 35)
# db_helper.add_user_model(1, "vvrvv", "rberbrv", 1, "grwbregergre")
# db_helper.add_chat(1, "vevev", 1)
# for i in range(15):
#     db_helper.add_message(1, "vrvrv", "erwverv")
# print(db_helper.amount_of_interaction())
