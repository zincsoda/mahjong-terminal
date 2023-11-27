import os

from users import UserClass
users = UserClass()
users.initialise_my_user_name()
print(users.get_users())
