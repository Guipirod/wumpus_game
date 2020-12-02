import pytest

from common.map_elements.actors.GameActor import GameActor
from common.map_elements.actors.Wumpus import Wumpus
from common.map_elements.items.Arrow import Arrow
from common.map_elements.items.Bow import Bow
from common.map_elements.items.Gold import Gold
from common.utils.functions import *


@pytest.mark.parametrize(
    "element_name,expected",
    [
        ("bow", True),
        ("arrow", True),
        ("gold", False),
        ("wumpus", False)
    ]
)
def test_player_has_item_with_name(element_name: str, expected: bool):
    bow_object = Bow(None, -1, -1)
    bow_object.in_inventory = True
    arrow_object = Arrow(None, -1, -1)
    arrow_object.in_inventory = True
    gold_object = Gold(None, -1, -1)
    wumpus_object = Wumpus(None, 0, 0)
    map_elements = [bow_object, arrow_object, gold_object, wumpus_object]

    assert player_has_item_with_name(map_elements, element_name) == expected, \
        f'Expected {"" if expected else "not "}to find "{element_name}" in inventory'


@pytest.mark.parametrize(
    "element_name,expected",
    [
        ("gold", True),
        ("wumpus", False)
    ]
)
def test_get_elements_in_player_coordinates(element_name: str, expected: bool):
    game_status = GameStatus('TestGame', height=2, width=2, silence_logger=True)
    game_status.player_x = 1
    game_status.player_y = 1

    gold_object = Gold(game_status, 1, 1)
    wumpus_object = Wumpus(game_status, 0, 0)
    map_elements = [gold_object, wumpus_object]

    names = [element.name for element in get_elements_in_player_coordinates(map_elements)]
    assert (element_name in names) == expected, \
        f'Expected {"" if expected else "not "}to find "{element_name}" in returned list'


@pytest.mark.parametrize(
    "element_name,expected",
    [
        ("bow", True),
        ("arrow", True),
        ("gold", False),
        ("wumpus", False)
    ]
)
def test_get_player_inventory(element_name: str, expected: bool):
    bow_object = Bow(None, -1, -1)
    bow_object.in_inventory = True
    arrow_object = Arrow(None, -1, -1)
    arrow_object.in_inventory = True
    gold_object = Gold(None, -1, -1)
    wumpus_object = Wumpus(None, 0, 0)
    map_elements = [bow_object, arrow_object, gold_object, wumpus_object]

    names = [element.name for element in get_player_inventory(map_elements)]
    assert (element_name in names) == expected, \
        f'Expected {"" if expected else "not "}to find "{element_name}" in returned list'


@pytest.mark.parametrize(
    "game_actor, alive, expected",
    [
        (Wumpus(None, 0, 0), True, True),
        (Wumpus(None, 0, 0), False, False),
        (Wumpus(None, 1, 1), True, False),
        (Wumpus(None, 1, 1), False, False)
    ]
)
def test_get_living_actors_in_coordinates(game_actor: GameActor, alive: bool, expected: bool):
    game_actor.alive = alive
    map_elements = [game_actor]

    assert (game_actor in get_living_actors_in_coordinates(map_elements, 0, 0)) == expected, \
        f'Expected function to return "{expected}" not "{not expected}"'


def test_delete_element_from_game():
    bow_object = Bow(None, -1, -1)
    arrow_object = Arrow(None, -1, -1)
    gold_object = Gold(None, -1, -1)
    wumpus_object = Wumpus(None, 0, 0)
    map_elements = [bow_object, arrow_object, gold_object, wumpus_object]

    delete_element_from_game(map_elements, bow_object)
    assert len(map_elements) == 3, f'Expected 3 map elements, but {len(map_elements)} were found'
    assert arrow_object in map_elements, f'Arrow object was deleted instead of Bow'
    assert gold_object in map_elements, f'Gold object was deleted instead of Bow'
    assert wumpus_object in map_elements, f'Wumpus object was deleted instead of Bow'


@pytest.mark.parametrize(
    "element_name,expected",
    [
        ("bow", False),
        ("arrow", True)
    ]
)
def test_drop_element_if_possible(element_name: str, expected: bool):
    game_status = GameStatus('TestGame', height=2, width=2, silence_logger=True)
    game_status.player_x = 1
    game_status.player_y = 1

    bow_object = Bow(game_status, -1, -1)
    bow_object.in_inventory = True
    arrow_object = Arrow(game_status, -1, -1)
    arrow_object.in_inventory = True
    map_elements = [bow_object, arrow_object]

    drop_element_if_possible(map_elements, 'bow')
    assert player_has_item_with_name(map_elements, element_name) == expected, \
        f'Expected {"" if expected else "not "}to find "{element_name}" in player inventory'


@pytest.mark.parametrize(
    "element_name,expected",
    [
        ("bow", False),
        ("arrow", True)
    ]
)
def test_take_map_element_if_possible(element_name: str, expected: bool):
    game_status = GameStatus('TestGame', height=2, width=2, silence_logger=True)
    game_status.player_x = 1
    game_status.player_y = 1

    bow_object = Bow(game_status, 0, 0)
    arrow_object = Arrow(game_status, 1, 1)
    map_elements = [bow_object, arrow_object]

    take_map_element_if_possible(game_status, map_elements, element_name)
    assert player_has_item_with_name(map_elements, element_name) == expected, \
        f'Expected {"" if expected else "not "}to find "{element_name}" in player inventory'


def test_get_first_inventory_element_with_name():
    bow_object_01 = Bow(None, 0, 0)
    bow_object_01.in_inventory = True
    bow_object_02 = Bow(None, 0, 0)
    bow_object_02.in_inventory = True
    arrow_object = Arrow(None, 0, 0)
    arrow_object.in_inventory = True
    map_elements = [bow_object_01, bow_object_02, arrow_object]

    assert bow_object_01 == get_first_inventory_element_with_name(map_elements, 'bow'), \
        'Function returned a reference to the wrong map element'


def test_get_first_map_element_in_player_position():
    game_status = GameStatus('TestGame', height=2, width=2, silence_logger=True)
    game_status.player_x = 1
    game_status.player_y = 1

    bow_object_01 = Bow(game_status, 0, 0)
    bow_object_02 = Bow(game_status, 1, 1)
    arrow_object = Arrow(game_status, 1, 1)
    map_elements = [bow_object_01, bow_object_02, arrow_object]

    assert bow_object_02 == get_first_map_element_in_player_position(map_elements, 'bow'), \
        'Function returned a reference to the wrong map element'
