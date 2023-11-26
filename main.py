import os

from users import UserClass
users = UserClass()
users.initialise_users()
print(users.get_users())