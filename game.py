from singleton import singleton


@singleton
class Game:

    def __init__(self, users):
        self.users = users

    def roll_dice(self):
        pass

    def get_all_user_positions(self):
        pass

    def get_all_user_visible_tiles(self):
        pass

    def get_my_tiles(self):
        pass