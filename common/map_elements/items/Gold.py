from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.items.GameItem import GameItem


class Gold(GameItem, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._hint_presence = 'You glimpse a suspicious shine near to your position'
        self._description = 'a brick of solid gold, worth a small fortune'
        self._player_use_event = "You can't use the gold, at least for now..."
        self._should_take_gold = "You should take the gold with you"

    @property
    def name(self):
        return 'gold'

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'g'

    def on_find(self):
        # What happens if the player and the element share the same space
        if not self.in_inventory:
            print(self._hint_presence)

    def on_use(self):
        # What happens if the player interacts with the element
        if self.in_inventory:
            print(self._player_use_event)
        else:
            print(self._should_take_gold)
