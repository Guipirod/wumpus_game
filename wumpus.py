import os
import json
import sys
from random import randint, choice

from common.map_elements.actors.Wumpus import Wumpus
from common.map_elements.basic.BottomlessPit import BottomlessPit
from common.map_elements.basic.GoldExit import GoldExit
from common.map_elements.items.Arrow import Arrow
from common.map_elements.items.Bow import Bow
from common.map_elements.items.Compass import Compass
from common.map_elements.items.Gold import Gold
from common.utils.functions import *

# GAME INITIALIZATION


def read_game_file(file_name: str) -> dict:
    with open(os.path.join('games', file_name)) as open_file:
        file_text = open_file.read()
    return json.loads(file_text)[file_name.replace('.json', '')]


def initialize_game_status(data_dict: dict) -> GameStatus:
    status = GameStatus(data_dict['GameName'], data_dict['GridScale']['height'], data_dict['GridScale']['width'])
    status.player_orientation = data_dict['PlayerData']['orientation']
    status.player_x = data_dict['PlayerData']['location']['x']
    status.player_y = data_dict['PlayerData']['location']['y']

    return status


def initialize_map_elements(data_dict: dict, game_status: GameStatus) -> list:
    map_elements = list()
    class_dictionary = get_class_dictionary()

    for element in data_dict["GridElements"]:
        position_x = element["location"]["x"]
        position_y = element["location"]["y"]
        game_element = class_dictionary[element["type"]](game_status, position_x, position_y)

        if "in_inventory" in element.keys():
            game_element.in_inventory = element['in_inventory']

        if "amount" in element.keys():
            game_element.amount = element['amount']

        map_elements.append(game_element)

    return map_elements


def initialize_aleatory_map() -> dict:
    game_data = dict()

    game_data["GameName"] = "RandomWumpus"
    game_data["GridScale"] = dict()
    game_data["GridScale"]["height"] = force_positive_int_input("Select map height in squares: ")
    game_data["GridScale"]["width"] = force_positive_int_input("Select map width in squares: ")

    forbidden_locations = list()  # positions taken by pits or the wumpus
    game_data["GridElements"] = list()

    # Generate pits
    maximum_pits = max(game_data["GridScale"]["height"]*game_data["GridScale"]["width"]-4, 0)
    total_pits = force_positive_int_input_with_threshold(f"Number of pits (max {maximum_pits}): ", maximum_pits)
    while total_pits > 0:
        element_x = randint(0, game_data["GridScale"]["height"]-1)
        element_y = randint(0, game_data["GridScale"]["width"]-1)
        if (element_x, element_y) not in forbidden_locations:
            total_pits -= 1
            forbidden_locations.append((element_x, element_y))
            game_data["GridElements"].append({"type": "BottomlessPit", "location": {"x": element_x, "y": element_y}})

    # Generate the wumpus
    while True:
        element_x = randint(0, game_data["GridScale"]["height"]-1)
        element_y = randint(0, game_data["GridScale"]["width"]-1)
        if (element_x, element_y) not in forbidden_locations:
            forbidden_locations.append((element_x, element_y))
            game_data["GridElements"].append({"type": "Wumpus", "location": {"x": element_x, "y": element_y}})
            break

    # Generate gold
    while True:
        element_x = randint(0, game_data["GridScale"]["height"]-1)
        element_y = randint(0, game_data["GridScale"]["width"]-1)
        if (element_x, element_y) not in forbidden_locations:
            game_data["GridElements"].append({"type": "Gold", "location": {"x": element_x, "y": element_y}})
            break

    # Generate exit, the exit must be situated in one of the grid's borders
    while True:
        grid_border = randint(0, 3)
        if grid_border == 0:
            element_x = 0
            element_y = randint(0, game_data["GridScale"]["width"] - 1)
        elif grid_border == 1:
            element_x = game_data["GridScale"]["height"]-1
            element_y = randint(0, game_data["GridScale"]["width"] - 1)
        elif grid_border == 2:
            element_x = randint(0, game_data["GridScale"]["height"] - 1)
            element_y = 0
        else:  # 3
            element_x = randint(0, game_data["GridScale"]["height"] - 1)
            element_y = game_data["GridScale"]["width"]-1

        if (element_x, element_y) not in forbidden_locations:
            game_data["GridElements"].append({"type": "GoldExit", "location": {"x": element_x, "y": element_y}})
            break

    # Generate initial equipment
    total_arrows = force_positive_int_input("Number of arrows: ")
    game_data["GridElements"].append({"type": "Arrow", "location": {"x": -1, "y": -1},
                                      "amount": total_arrows, "in_inventory": True})
    game_data["GridElements"].append({"type": "Bow", "location": {"x": -1, "y": -1}, "in_inventory": True})

    # Generate initial position
    game_data["PlayerData"] = dict()
    game_data["PlayerData"]["location"] = dict()
    while True:
        element_x = randint(0, game_data["GridScale"]["height"] - 1)
        element_y = randint(0, game_data["GridScale"]["width"] - 1)
        if (element_x, element_y) not in forbidden_locations:
            game_data["PlayerData"]["location"]["x"] = element_x
            game_data["PlayerData"]["location"]["y"] = element_y
            break
    game_data["PlayerData"]["orientation"] = choice(("N", "S", "W", "E"))

    return game_data

# PRINT WUMPUS MAP


def print_map(game_status: GameStatus, map_elements: list):
    print(f'Player on ({game_status.player_x}, {game_status.player_y})')
    print(f'Player looking "{game_status.player_orientation}"')

    if game_status.player_orientation == 'N':
        player_token = '^'
    elif game_status.player_orientation == 'S':
        player_token = 'v'
    elif game_status.player_orientation == 'W':
        player_token = '<'
    else:
        player_token = '>'

    map_representation = list()
    for i in range(game_status.map_height):
        map_representation.append(['.'] * game_status.map_width)

    for element in map_elements:
        if not (hasattr(element, 'in_inventory') and element.in_inventory):
            map_representation[element.position_x][element.position_y] = element.map_character

    map_representation[game_status.player_x][game_status.player_y] = player_token

    aux_print = list()
    for row in map_representation:
        aux_print.append(' '.join(row))

    print('\n'.join(aux_print))


# PRIMARY LOOP

def interpret_player_input(game_status: GameStatus, map_elements: list):
    player_input = input(">>> ").split(' ')

    log_player_action = True
    if player_input[0] == 'exit':
        sys.exit()
    elif player_input[0] in ('advance', 'walk'):
        game_status.advance_player()
    elif player_input[0] == 'turn' and len(player_input) == 2:
        game_status.rotate_player(player_input[1])
    elif player_input[0] == 'use' and len(player_input) == 2:
        use_element_if_found(game_status, map_elements, player_input[1])
    elif player_input[0] in ('inventory', 'inv'):
        print_player_inventory(map_elements)
    elif player_input[0] in ('look', 'describe') and len(player_input) == 2:
        if player_input[1] == 'around':
            describe_elements_in_location(map_elements)
        else:
            describe_element_if_found(map_elements, player_input[1])
    elif player_input[0] == 'take' and len(player_input) == 2:
        take_map_element_if_possible(game_status, map_elements, player_input[1])
    elif player_input[0] == 'drop' and len(player_input) == 2:
        drop_element_if_possible(map_elements, player_input[1])

    else:
        print("You can't do that now...")
        log_player_action = False

    print()
    if log_player_action:
        game_status.logger.log(' '.join(player_input))


def primary_loop(game_status: GameStatus, map_elements: list, debug_mode_on: bool):
    while True:

        call_found_elements_functions(game_status, map_elements)
        game_status.end_game_if_triggered()
        call_near_elements_functions(game_status, map_elements)
        game_status.end_game_if_triggered()

        if debug_mode_on:
            print_map(game_status, map_elements)

        interpret_player_input(game_status, map_elements)

        game_status.end_game_if_triggered()

# MAIN


def main():

    debug_mode_on = '--debug' in sys.argv

    player_choice = input("Enter a file name to load, or press ENTER to generate the map:\n>>> ")

    if player_choice:
        game_data = read_game_file(player_choice)
    else:
        game_data = initialize_aleatory_map()

    game_status = initialize_game_status(game_data)
    map_elements = initialize_map_elements(game_data, game_status)

    print("You are walking in the woods...")
    print("There is nobody around and your phone is dead")

    primary_loop(game_status, map_elements, debug_mode_on)


if __name__ == '__main__':
    main()
