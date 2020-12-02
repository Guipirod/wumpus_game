from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.items.GameItem import GameItem


class Compass(GameItem, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._cardinal_directions = {"N": "north", "S": "south", "W": "west", "E": "east"}

        self._description = "a compass, can help you to orientate"
        self._hint_presence = "There is a compass on the ground"
        self._take_compass = "You must take the compass to use it"
        self._orientation = "You check the compass, you are facing {}"

    @property
    def name(self):
        return "compass"

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'c'

    def on_find(self):
        # What happens if the player and the element share the same space
        if not self.in_inventory:
            print(self._hint_presence)

    def on_use(self):
        if self.in_inventory:
            print(self._orientation.format(
                self._cardinal_directions[self.game_status.player_orientation]))
        else:
            print(self._take_compass)
