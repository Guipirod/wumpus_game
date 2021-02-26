from abc import ABC

from common.game_status import GameStatus
from common.map_elements.map_element import MapElement


class BottomlessPit(MapElement, ABC):

    _player_death_event = 'You trip and fall in a bottomless dark pit\n' \
                               'Your scream echoes in the dark forest, but no help comes...\n\n' \
                               'YOU ARE DEAD'
    _description = 'a pitch black bottomless pit'
    _pit_breeze = 'You feel a cold breeze coming from somewhere nearby'
    _log_death = 'You were killed falling into a pit'

    @property
    def name(self):
        return 'pit'

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'p'

    def on_find(self):
        # What happens if the player and the element share the same space
        print(self._player_death_event)
        self.game_status.trigger_game_end(self._log_death)

    def on_proximity(self):
        # What happens if the element is near the player
        print(self._pit_breeze)
