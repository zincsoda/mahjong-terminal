from singleton import singleton
import os

config_file = "user.config"

all_users = {
    'across': 'Alison',
    'left': 'Lisa',
    'right': 'Ralf'
}

@singleton
class UserClass:

    def __init__(self):
        self.my_user = ""

    def _check_if_user_saved(self):
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config_data = file.readlines()
            for line in config_data:
                if line.startswith("name="):
                    existing_name = line.split("=")[1].strip()
                    return existing_name
        return None
            
    def _confirm_user(self, saved_user):
        user_input = input(f"Do you wish to continue as '{saved_user}'? (y/n): ")
        if user_input.lower() == "y" or user_input == "":
            return saved_user
        
    def _enter_user(self):
        my_user = input("Enter a new name: ")
        with open(config_file, "w") as file:
            file.write(f"name={my_user}")
        return my_user

    def initialise_my_user_name(self):
        saved_user = self._check_if_user_saved()
        if saved_user and self._confirm_user(saved_user):            
            self.my_user = saved_user
        else:
            self.my_user = self._enter_user()

    def get_users(self):
        all_users['self'] = self.my_user
        return(all_users)
                
 