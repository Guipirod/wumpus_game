from abc import ABC
from random import choice

from common.game_status import GameStatus
from common.map_elements.actors.game_actor import GameActor


class ShiaLaBeouf(GameActor, ABC):

    _player_death_event = 'Hollywood superstar Shia LaBeouf catches you off guard\n\n' \
                               'YOU ARE DEAD'
    _shia_death_event = 'You hear an unmistakable scream, are you finally safe from Shia LaBeouf?'
    _resurrection_event = "Wait, he isn't dead, shia-surprise!"
    _movement_event = 'He\'s gaining on you'
    _alive_description = 'actual cannibal Shia LaBeouf'
    _dead_description = 'the corpse of actual cannibal Shia LaBeouf'
    _log_fake_death = 'Shia LaBeouf was shot, not killed'
    _log_read_death = 'Shia LaBeouf was killed'
    _log_resurrection = 'Shia LaBeouf resurrected'
    _log_player_death = 'You were killed by Shia LaBeouf'
    _log_shia_movement = 'Shia LaBeouf moves to ({}, {})'
    _random_song_phrase = [
        'He\'s following you\nAbout thirty feet back',
        'He\'s brandishing a knife\nIt\'s Shia LaBeouf',
        'Lurking in the shadows\nHollywood superstar Shia LaBeouf',
        'Sharpening an ax\nShia LaBeouf',
    ]

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)
        self._resurrected = False
        self._revive_counter = 0
        self._next_x = None
        self._next_y = None
        self._movement_triggered = False
        self._waiting_to_move = False

    @property
    def name(self) -> str:
        return "shia"

    @property
    def description(self):
        return self._alive_description if self.alive else self._dead_description

    @property
    def map_character(self) -> str:
        return 's'

    def on_death(self):
        self.alive = False
        print(self._shia_death_event)
        if self._resurrected:
            self.game_status.logger.log(self._log_read_death, player_action=False)
        else:
            self._resurrected = True
            self._revive_counter = 3
            self.game_status.logger.log(self._log_fake_death, player_action=False)

    def on_find(self):
        # What happens if the player and the element share the same space
        if self.alive:
            print(self._player_death_event)
            self.game_status.trigger_game_end(self._log_player_death)
        else:
            print(f"You find {self._dead_description}")

    def on_proximity(self):
        if self.alive:
            print(choice(self._random_song_phrase))
            if not self._movement_triggered:
                self._movement_triggered = True
                self._next_x = self.game_status.player_x
                self._next_y = self.game_status.player_y
                self._waiting_to_move = True

    def act(self):
        if self.alive:
            if self._movement_triggered:
                if self._waiting_to_move:
                    self._waiting_to_move = False
                else:
                    self.position_x = self._next_x
                    self.position_y = self._next_y
                    self._movement_triggered = False
                    print(self._movement_event)
                    self.game_status.logger.log(self._log_shia_movement.format(self.position_y, self.position_y),
                                                player_action=False)
        else:
            if self._revive_counter == 0:
                self.alive = True
                print(self._resurrection_event)
                self.game_status.logger.log(self._log_resurrection, player_action=False)
            else:
                self._revive_counter -= 1
