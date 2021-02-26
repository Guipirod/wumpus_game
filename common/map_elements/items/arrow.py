from abc import ABC

from common.game_status import GameStatus
from common.map_elements.items.game_item import GameItem


class Arrow(GameItem, ABC):

    _description = 'a pointy arrow, ammunition for a bow'
    _hint_presence = 'You see some arrows on the ground'
    _player_use_event = 'You need a bow in order to use an arrow'

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
