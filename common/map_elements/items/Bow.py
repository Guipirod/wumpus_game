from abc import ABC

from common.GameStatus import GameStatus
from common.map_elements.items.GameItem import GameItem
from common.utils.functions import get_living_actors_in_coordinates, get_first_inventory_element_with_name, \
    delete_element_from_game


class Bow(GameItem, ABC):

    def __init__(self, game_status: GameStatus, position_x: int, position_y: int):
        super().__init__(game_status, position_x, position_y)

        self._description = 'a bow, you can fire it if you happen to have arrows'
        self._hint_presence = 'You see a bow laying on the floor near your feet'
        self._player_use_event = 'You aim to the darkness and shoot your bow'
        self._no_target = 'But nothing happens...'
        self._no_arrows = 'You are out of arrows...'
        self._take_first_hint = 'You should take the bow from the ground if you want to use it'

    @property
    def name(self):
        return 'bow'

    @property
    def description(self):
        return self._description

    @property
    def map_character(self) -> str:
        return 'b'

    def _shoot_arrow(self, game_status: GameStatus, map_elements: list):
        # calculate arrow starting point and how it advances
        advance_x = self.game_status.advance[self.game_status.player_orientation]['x']
        advance_y = self.game_status.advance[self.game_status.player_orientation]['y']
        projectile_x = self.game_status.player_x + advance_x
        projectile_y = self.game_status.player_y + advance_y

        # make the arrow advance until it hits and kills another actor or leaves the map
        while 0 <= projectile_x < self.game_status.map_width and 0 <= projectile_y < self.game_status.map_height:
            actors = get_living_actors_in_coordinates(map_elements, projectile_x, projectile_y)
            if len(actors) > 0:
                actors[0].on_death()  # if more than one actor share location the first one will be hit
                break

            projectile_x += advance_x
            projectile_y += advance_y

        else:
            print(self._no_target)

    def on_use(self):
        def foo(game_status: GameStatus, map_elements: list):
            if self.in_inventory:
                arrow_item = get_first_inventory_element_with_name(map_elements, 'arrow')

                if arrow_item is not None:
                    print(self._player_use_event)
                    self._shoot_arrow(game_status, map_elements)

                    # remove an arrow from the player's inventory
                    if arrow_item.amount < 2:
                        delete_element_from_game(map_elements, arrow_item)
                    else:
                        arrow_item.amount -= 1
                else:
                    print(self._no_arrows)
            else:
                print(self._take_first_hint)

        return foo
