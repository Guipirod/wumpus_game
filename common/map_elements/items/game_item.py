from abc import ABC

from common.game_status import GameStatus
from common.map_elements.map_element import MapElement
from common.utils.functions import get_first_inventory_element_with_name, get_player_inventory, \
    get_first_map_element_in_player_position


class GameItem(MapElement, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int, in_inventory: bool = False, amount: int = 1):
        super().__init__(game_status, position_x, position_y)

        self.in_inventory = in_inventory
        self.amount = amount

    def on_take(self):
        self.in_inventory = True
        print(f"You took {self.name} (x{self.amount})")

        def merge_inventory_copies(_, map_elements: list):
            target_element = get_first_inventory_element_with_name(map_elements, self.name)
            delete_indexes = list()
            for index in range(len(map_elements)):
                if map_elements[index].name == target_element.name and hasattr(map_elements[index], 'in_inventory') \
                        and map_elements[index].in_inventory and map_elements[index] != target_element:
                    delete_indexes.append(index)
                    target_element.amount += map_elements[index].amount

            delete_indexes.reverse()
            for index in delete_indexes:
                del map_elements[index]

        return merge_inventory_copies

    def on_drop(self):
        self.in_inventory = False
        self.position_x = self.game_status.player_x
        self.position_y = self.game_status.player_y
        print(f"You drop {self.name} (x{self.amount})")

        def merge_ground_copies(_, map_elements: list):
            target_element = get_first_map_element_in_player_position(map_elements, self.name)
            delete_indexes = list()
            for index in range(len(map_elements)):
                if map_elements[index].name == target_element.name and \
                        map_elements[index].in_position(self.position_x, self.position_y) and \
                        not (hasattr(map_elements[index], 'in_inventory') and map_elements[index].in_inventory) \
                        and map_elements[index] != target_element:
                    delete_indexes.append(index)
                    target_element.amount += map_elements[index].amount

            delete_indexes.reverse()
            for index in delete_indexes:
                del map_elements[index]

        return merge_ground_copies

    def with_player(self) -> bool:
        if self.in_inventory:
            return True
        else:
            return self.in_position(self.game_status.player_x, self.game_status.player_y)

    def near_player(self) -> bool:
        # An element taken by the player should not be "near" the player but "on" the player
        if self.in_inventory:
            return False
        else:
            return self.near_position(self.game_status.player_x, self.game_status.player_y)

    def in_position(self, x, y) -> bool:
        if self.in_inventory:
            return self.game_status.player_x == x and self.game_status.player_y == y
        else:
            return self.position_x == x and self.position_y == y

    def near_position(self, x, y) -> bool:
        if self.in_inventory:
            return abs(self.game_status.player_y - y) <= 1 and abs(self.game_status.player_x - x) <= 1
        else:
            return abs(self.position_y - y) <= 1 and abs(self.position_x - x) <= 1