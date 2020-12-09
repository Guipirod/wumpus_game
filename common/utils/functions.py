from inspect import ismodule, isclass, getmembers

from common.GameStatus import GameStatus
from common.map_elements import actors
from common.map_elements import basic
from common.map_elements import items


def force_positive_int_input(message: str) -> int:
    player_input = ''
    while not player_input.isdigit():
        player_input = input(message)
    return int(player_input)


def force_positive_int_input_with_threshold(message: str, upper_limit: int) -> int:
    player_input = force_positive_int_input(message)
    while player_input > upper_limit:
        print(f'Choose a number <={upper_limit}')
        player_input = force_positive_int_input(message)
    return player_input


def get_player_inventory(map_elements: list) -> list:
    return [element for element in map_elements if hasattr(element, 'in_inventory') and element.in_inventory]


def player_has_item_with_name(map_elements: list, name: str) -> bool:
    inventory = get_player_inventory(map_elements)
    return any(filter(lambda x: x.name == name, inventory))


def get_elements_in_player_coordinates(map_elements: list) -> list:
    return [element for element in map_elements if element.with_player() and not (hasattr(element, 'in_inventory')
                                                                                  and element.in_inventory)]


def get_living_actors_in_coordinates(map_elements: list, x: int, y: int) -> list:
    return [element for element in map_elements if
            hasattr(element, 'alive') and element.alive and element.in_position(x, y)]


def get_first_inventory_element_with_name(map_elements: list, name: str):
    for element in get_player_inventory(map_elements):
        if element.name == name:
            return element


def get_first_map_element_in_player_position(map_elements: list, name: str):
    for element in get_elements_in_player_coordinates(map_elements):
        if element.name == name:
            return element


def delete_element_from_game(map_elements: list, element):
    for i in range(len(map_elements)):
        if map_elements[i] == element:
            del map_elements[i]
            break


def drop_element_if_possible(map_elements: list, name: str):
    for element in get_player_inventory(map_elements):
        if element.name == name:
            element.on_drop()
        break
    else:
        print(f"You have no {name} to drop")


def take_map_element_if_possible(game_status: GameStatus, map_elements: list, name: str):
    for element in get_elements_in_player_coordinates(map_elements):
        if hasattr(element, 'in_inventory') and element.name == name:
            result = element.on_take()
            if callable(result):
                result(game_status, map_elements)
            break
    else:
        print("You can't do that")


def call_found_elements_functions(game_status: GameStatus, map_elements: list):
    for element in map_elements:
        if element.with_player():
            result = element.on_find()
            if callable(result):
                result(game_status, map_elements)


def call_near_elements_functions(game_status: GameStatus, map_elements: list):
    for element in map_elements:
        if element.near_player():
            result = element.on_proximity()
            if callable(result):
                result(game_status, map_elements)


def use_element(game_status: GameStatus, map_elements: list, map_element):
    result = map_element.on_use()
    if callable(result):
        result(game_status, map_elements)


def use_element_if_found(game_status: GameStatus, map_elements: list, expected_name: str):
    in_inventory = [element for element in get_player_inventory(map_elements) if element.name == expected_name]
    in_location = [element for element in get_elements_in_player_coordinates(map_elements) if element.name == expected_name]

    if len(in_inventory) > 0 and len(in_location) > 0:
        decision = None
        while decision not in ('I', 'G'):
            decision = input("The one on your inventory (I) or the ground (G)?: ").split(' ')[0]
        if decision == 'G':
            use_element(game_status, map_elements, in_location[0])
        else:
            use_element(game_status, map_elements, in_inventory[0])
    elif len(in_inventory) > 0:
        use_element(game_status, map_elements, in_inventory[0])
    elif len(in_location) > 0:
        use_element(game_status, map_elements, in_location[0])
    else:
        print(f'You have no "{expected_name}"')


def describe_element_if_found(map_elements: list, expected_name: str):
    in_inventory = [element for element in get_player_inventory(map_elements) if element.name == expected_name]
    in_location = [element for element in get_elements_in_player_coordinates(map_elements) if
                   element.name == expected_name]

    if len(in_inventory) > 0:
        print(f'You see {in_inventory[0].description}')
    elif len(in_location) > 0:
        print(f'You see {in_location[0].description}')
    else:
        print(f'You have no "{expected_name}"')


def describe_elements_in_location(map_elements: list):
    for element in get_elements_in_player_coordinates(map_elements):
        print(f"You see {element.description}")


def print_player_inventory(map_elements: list):
    summary = [f'{e.name} {f"({e.amount})" if hasattr(e, "amount") else ""}' for e in get_player_inventory(map_elements)]
    print("Inventory:")
    print('\n'.join(summary) + '\n')


def get_class_dictionary() -> dict:
    class_dictionary = dict()

    for package in [actors, basic, items]:
        for module_name, module in [m for m in getmembers(package, ismodule) if m[1].__package__ == package.__name__]:
            for class_name, cls in [c for c in getmembers(module, isclass) if c[1].__module__ == module.__name__]:
                class_dictionary[class_name] = cls

    return class_dictionary

