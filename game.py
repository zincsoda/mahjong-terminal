from singleton import singleton
import random


@singleton
class Game:

    def __init__(self, users):
        self.users = users

    def _roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        return dice1, dice2

    def roll_dice(self):
        highest_roll = 0
        highest_user = None
        for user_key in self.users.keys():
            roll = self._roll_dice()
            combined_roll = roll[0] + roll[1]
            print(self.users[user_key], "rolled", roll[0], "and", roll[1], "for a total of", combined_roll)            
            if  combined_roll > highest_roll:
                highest_roll = combined_roll
                highest_user = self.users[user_key]
        print(highest_user, "is the East Wind")
        return highest_user

    def get_all_user_positions(self):
        pass

    def get_all_user_visible_tiles(self):
        pass

    def get_my_tiles(self):
        pass

users = {'across': 'Alison', 'left': 'Lisa', 'right': 'Ralf', 'self': 'Steve'}
game = Game(users)
game.roll_dice()