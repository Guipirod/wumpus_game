from sys import exit
from common.logger import Logger


class GameStatus:

    def __init__(self, game_name: str, height: int = 5, width: int = 5, silence_logger: bool = False):
        self.endgame_triggered = False
        self.endgame_message = ''

        self.player_x = 0
        self.player_y = 0
        self.player_orientation = 'N'  # N, W, E, S
        self.advance = {
            'N': {'x': -1, 'y': 0},
            'S': {'x': 1, 'y': 0},
            'E': {'x': 0, 'y': 1},
            'W': {'x': 0, 'y': -1}
        }

        self.map_height = height
        self.map_width = width

        self.game_vars = dict()

        self.logger = Logger(game_name, silence=silence_logger)
        self.actions = 0

    def trigger_game_end(self, endgame_message: str):
        self.endgame_triggered = True
        self.endgame_message = endgame_message

    def end_game_if_triggered(self):
        if self.endgame_triggered:
            self.logger.log(self.endgame_message, player_action=False)
            exit()

    def rotate_player(self, direction: str):
        if direction in ('left', 'right'):
            self.actions += 1
            print(f"You turn {direction}")
            if self.player_orientation == 'N':
                self.player_orientation = 'E' if direction == 'right' else 'W'
            elif self.player_orientation == 'W':
                self.player_orientation = 'N' if direction == 'right' else 'S'
            elif self.player_orientation == 'S':
                self.player_orientation = 'W' if direction == 'right' else 'E'
            else:  # player_orientation == 'E
                self.player_orientation = 'S' if direction == 'right' else 'N'
        else:
            print("You can only turn left or right")

    def advance_player(self):
        self.actions += 1
        expected_x = self.advance[self.player_orientation]['x']
        expected_y = self.advance[self.player_orientation]['y']
        if 0 <= self.player_x + expected_x < self.map_height and 0 <= self.player_y + expected_y < self.map_width:
            self.player_x += expected_x
            self.player_y += expected_y
        else:
            print("You try to advance, but the forest is far too dense from this point on")
