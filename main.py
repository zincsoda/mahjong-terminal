from users import UserClass
from game import Game

users = UserClass()
users.initialise_my_user_name()
all_users = users.get_users()
print("Players:", all_users)

game = Game(all_users)
winner = game.play_round()

if winner is None:
    print("No winner this round.")
else:
    print(f"Winner: {winner}")
