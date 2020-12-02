from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.MapElement import MapElement
from common.utils.functions import player_has_item_with_name


class GoldExit(MapElement, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._player_victory_event = "You have your gold, you avoided the monster...\n" \
                                     "Now you can safely run away and leave this wretched place.\n\n" \
                                     "YOU WIN"
        self._player_needs_gold = "You came to this forest looking for gold, and you are not going to " \
                                  "run away empty-handed"
        self._description = "an exit, a safe scape from this dark forest"
        self._log_victory = "You won by exiting the forest"

    @property
    def name(self):
        return 'exit'

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'e'

    def on_find(self):
        print(f"You find yourself near {self._description}")

    def on_use(self):
        # What happens if the player interacts with the element

        def foo(game_status: GameStatus, map_elements: list):
            if player_has_item_with_name(map_elements, 'gold'):
                print(self._player_victory_event)
                game_status.trigger_game_end(self._log_victory)
            else:
                print(self._player_needs_gold)

        return foo
