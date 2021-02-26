from abc import abstractmethod

from common.game_status import GameStatus


class MapElement:

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        self.position_x = position_x
        self.position_y = position_y
        self.game_status = game_status

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def map_character(self) -> str:
        return '?'

    @abstractmethod
    def on_find(self):
        # What happens if the player and the element share the same space
        # Can either return nothing or a function(GameStatus, map_elements) that has to be run
        pass

    @abstractmethod
    def on_proximity(self):
        # What happens if the element is near the player
        # Can either return nothing or a function(GameStatus, map_elements) that has to be run
        pass

    @abstractmethod
    def on_use(self):
        # What happens if the player interacts with the element
        # Can either return nothing or a function(GameStatus, map_elements) that has to be run
        print(f"You can't use the {self.name} for anything")

    @abstractmethod
    def act(self):
        # Useful if we need to implement an element that has its own movements instead of being passive
        # Can either return nothing or a function(GameStatus, map_elements) that has to be run
        pass

    def with_player(self) -> bool:
        return self.in_position(self.game_status.player_x, self.game_status.player_y)

    def near_player(self) -> bool:
        return self.near_position(self.game_status.player_x, self.game_status.player_y)

    def in_position(self, x, y) -> bool:
        return self.position_x == x and self.position_y == y

    def near_position(self, x, y) -> bool:
        return bool(y==self.position_y and (x == self.position_x+1 or x == self.position_x-1)) != bool(x==self.position_x and (y == self.position_y+1 or y == self.position_y-1))
