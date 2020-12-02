from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.items.GameItem import GameItem


class Arrow(GameItem, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._description = 'a pointy arrow, ammunition for a bow'
        self._hint_presence = 'You see some arrows on the ground'
        self._player_use_event = 'You need a bow in order to use an arrow'

    @property
    def name(self):
        return 'arrow'

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'a'

    def on_find(self):
        # What happens if the player and the element share the same space
        if not self.in_inventory:
            print(self._hint_presence)

    def on_use(self):
        # What happens if the player interacts with the element
        if self.in_inventory:
            print(self._player_use_event)
