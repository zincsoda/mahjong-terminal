import random
import unicodedata


class Game:
    DOT_TILES = ("1☉", "2☉", "3☉", "4☉", "5☉", "6☉", "7☉", "8☉", "9☉")
    BAMBOO_TILES = ("1⑊", "2⑊", "3⑊", "4⑊", "5⑊", "6⑊", "7⑊", "8⑊", "9⑊")
    CHARACTER_TILES = ("一", "二", "三", "四", "五", "六", "七", "八", "九")
    WIND_TILES = ("东", "南", "西", "北")
    DRAGON_TILES = ("中", "青", "白")

    SUIT_TILE_GROUPS = (DOT_TILES, BAMBOO_TILES, CHARACTER_TILES)
    HONOR_TILES = WIND_TILES + DRAGON_TILES
    ALL_TILE_TYPES = DOT_TILES + BAMBOO_TILES + CHARACTER_TILES + HONOR_TILES
    SEAT_ORDER = ("east", "south", "west", "north")

    def __init__(self, users):
        self.users = users
        self.player_hands = {}
        self.player_discards = {}
        self.seat_players = {}
        self.wall = []
        self.turn_index = 0
        self.tile_to_index_map = {tile: index for index, tile in enumerate(self.ALL_TILE_TYPES)}

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

    def _build_wall(self):
        wall = []
        for suit_tiles in self.SUIT_TILE_GROUPS:
            for tile in suit_tiles:
                wall.extend([tile] * 3)
        for honor in self.HONOR_TILES:
            wall.extend([honor] * 4)
        random.shuffle(wall)
        return wall

    def _sort_tiles(self, tiles):
        return sorted(tiles, key=self._tile_to_index)

    def _is_suited_tile(self, tile):
        return self._tile_to_index(tile) < 27

    def _find_melds(self, counts):
        remaining = [i for i, value in enumerate(counts) if value > 0]
        if not remaining:
            return True

        first = remaining[0]

        if counts[first] >= 3:
            counts[first] -= 3
            if self._find_melds(counts):
                counts[first] += 3
                return True
            counts[first] += 3

        if first < 27:
            position_in_suit = first % 9
            if position_in_suit <= 6:
                next1 = first + 1
                next2 = first + 2
                if counts[next1] > 0 and counts[next2] > 0:
                    counts[first] -= 1
                    counts[next1] -= 1
                    counts[next2] -= 1
                    if self._find_melds(counts):
                        counts[first] += 1
                        counts[next1] += 1
                        counts[next2] += 1
                        return True
                    counts[first] += 1
                    counts[next1] += 1
                    counts[next2] += 1
        return False

    def _tile_to_index(self, tile):
        return self.tile_to_index_map[tile]

    def _tile_from_index(self, index):
        return self.ALL_TILE_TYPES[index]

    def is_standard_win(self, hand):
        if len(hand) != 14:
            return False

        counts = [0] * 34
        for tile in hand:
            counts[self._tile_to_index(tile)] += 1

        for pair_index in range(34):
            if counts[pair_index] >= 2:
                counts[pair_index] -= 2
                if self._find_melds(counts):
                    counts[pair_index] += 2
                    return True
                counts[pair_index] += 2
        return False

    def setup_round(self):
        east_player = self.roll_dice()
        ordered_players = [east_player]
        for user_name in self.users.values():
            if user_name != east_player:
                ordered_players.append(user_name)

        self.seat_players = {
            self.SEAT_ORDER[index]: player_name
            for index, player_name in enumerate(ordered_players)
        }
        self.player_hands = {player_name: [] for player_name in ordered_players}
        self.player_discards = {player_name: [] for player_name in ordered_players}
        self.wall = self._build_wall()

        for _ in range(13):
            for seat in self.SEAT_ORDER:
                player_name = self.seat_players[seat]
                self.player_hands[player_name].append(self.wall.pop())

        for player_name in self.player_hands:
            self.player_hands[player_name] = self._sort_tiles(self.player_hands[player_name])
        self.turn_index = 0

    def get_all_user_positions(self):
        return self.seat_players

    def get_all_user_visible_tiles(self):
        return self.player_discards

    def get_my_tiles(self):
        my_name = self.users.get("self")
        if not my_name:
            return []
        return self.player_hands.get(my_name, [])

    def _print_state(self):
        print("\nSeat positions:")
        for seat in self.SEAT_ORDER:
            print(f"- {seat}: {self.seat_players[seat]}")
        print(f"Tiles left in wall: {len(self.wall)}")

    def _print_hand_with_boxes(self, hand, tiles_per_row=8):
        inner_width = 6
        top_border = "┌" + ("─" * inner_width) + "┐"
        bottom_border = "└" + ("─" * inner_width) + "┘"

        def display_width(text):
            total = 0
            for char in text:
                if unicodedata.east_asian_width(char) in ("W", "F"):
                    total += 2
                else:
                    total += 1
            return total

        def center_for_terminal(text, width):
            text_width = display_width(text)
            if text_width >= width:
                return text
            total_padding = width - text_width
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            return (" " * left_padding) + text + (" " * right_padding)

        for row_start in range(0, len(hand), tiles_per_row):
            row_tiles = hand[row_start:row_start + tiles_per_row]
            top_line = " ".join(top_border for _ in row_tiles)
            middle_line = " ".join(f"│{center_for_terminal(tile, inner_width)}│" for tile in row_tiles)
            bottom_line = " ".join(bottom_border for _ in row_tiles)
            index_line = " ".join(
                f" {center_for_terminal(str(index), inner_width)} "
                for index in range(row_start, row_start + len(row_tiles))
            )

            print(top_line)
            print(middle_line)
            print(bottom_line)
            print(index_line)
            print("")

    def _choose_discard(self, player_name):
        hand = self.player_hands[player_name]
        if player_name == self.users.get("self"):
            while True:
                print(f"\nYour hand ({len(hand)} tiles):")
                self._print_hand_with_boxes(hand)
                user_input = input("Choose tile index to discard (enter for auto): ").strip()
                if user_input == "":
                    return random.randrange(len(hand))
                if user_input.isdigit():
                    discard_index = int(user_input)
                    if 0 <= discard_index < len(hand):
                        return discard_index
                print("Invalid choice. Try again.")
        return random.randrange(len(hand))

    def _run_turn(self, player_name):
        drawn_tile = self.wall.pop()
        self.player_hands[player_name].append(drawn_tile)
        self.player_hands[player_name] = self._sort_tiles(self.player_hands[player_name])
        print(f"\n{player_name} draws {drawn_tile}")

        if self.is_standard_win(self.player_hands[player_name]):
            print(f"{player_name} wins by tsumo!")
            return True

        discard_index = self._choose_discard(player_name)
        discarded_tile = self.player_hands[player_name].pop(discard_index)
        self.player_discards[player_name].append(discarded_tile)
        print(f"{player_name} discards {discarded_tile}")
        return False

    def play_round(self):
        self.setup_round()
        self._print_state()
        print("\nRound start! Each player has 13 tiles.")

        while self.wall:
            seat = self.SEAT_ORDER[self.turn_index]
            current_player = self.seat_players[seat]
            if self._run_turn(current_player):
                return current_player
            self.turn_index = (self.turn_index + 1) % 4

        print("Round ends in an exhaustive draw.")
        return None