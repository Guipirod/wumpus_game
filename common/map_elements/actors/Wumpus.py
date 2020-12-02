from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.actors.GameActor import GameActor


class Wumpus(GameActor, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._player_death_event = 'Suddenly an indescribable monster jumps on you from its hiding\n' \
                                   'You try to scream for help, but there is no use...\n\n' \
                                   'YOU ARE DEAD'
        self._wumpus_death_event = 'A loud scream is heard all over the forest'
        self._dead_description = 'the dead body of the wumpus, or so you hope'
        self._alive_description = 'the wumpus, a hideous man eating monster'
        self._wumpus_scent = 'You smell a nauseous scent nearby...'
        self._log_player_death = 'You were killed by the wumpus'
        self._log_wumpus_death = 'The wumpus was killed'

    @property
    def name(self):
        return 'wumpus'

    @property
    def description(self):
        return self._alive_description if self.alive else self._dead_description

    @property
    def map_character(self) -> str:
        return 'w'

    def on_death(self):
        self.alive = False
        print(self._wumpus_death_event)
        self.game_status.logger.log(self._log_wumpus_death, player_action=False)

    def on_find(self):
        # What happens if the player and the element share the same space
        if self.alive:
            print(self._player_death_event)
            self.game_status.trigger_game_end(self._log_player_death)
        else:
            print(f"You find {self._dead_description}")

    def on_proximity(self):
        # What happens if the element is near the player
        print(self._wumpus_scent)
