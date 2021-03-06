from abc import ABC, abstractmethod

from common.game_status import GameStatus
from common.map_elements.map_element import MapElement


class GameActor(MapElement, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self.alive = True

    @abstractmethod
    def on_death(self):
        self.alive = False
