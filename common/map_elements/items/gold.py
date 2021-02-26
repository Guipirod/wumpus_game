from abc import ABC

from common.game_status import GameStatus
from common.map_elements.items.game_item import GameItem


class Gold(GameItem, ABC):

    _hint_presence = 'You glimpse a suspicious shine near to your position'
    _description = 'a brick of solid gold, worth a small fortune'
    _player_use_event = "You can't use the gold, at least for now..."
    _should_take_gold = "You should take the gold with you"

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
