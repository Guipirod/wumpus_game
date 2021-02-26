Wumpus
======

An overly complicated implementation of the [wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus) game.

## How to run

To properly run this program you first have to install Python 3.6 (or [newer](https://www.python.org/downloads/) version) and [pip](https://pypi.org/project/pip/).
Download the game then move to its root directory and install the dependencies with:

```pip install -r requirements.txt```

Execute the game by running:

```python wumpus_game.py```

Logs of each game will be saved on the **/logs** folder.

You can load one of the predefined games on the **/games** folder by typing its name when the program starts, or generate the map randomly by pressing **ENTER**.

If you want to create you own predefined game use the existing ones as a reference. Just notice that the map is a list of lists that is drawn from top to bottom, and therefore coordinates work different:

```
x0  .  .  .  
x1  .  .  .
x2  .  .  .
x3  .  .  .
   y0 y1 y2
```

Both the arrows and the bow are not in the player's inventory by default, remember to configure them properly like this:

```
{
    "type": "Arrow",
    "location": {"x": -1, "y": -1},     # location is irrelevant while on inventory
    "in_inventory": true,               # false by default
    "amount": 5                         # 1 by default
}
```

## How to play

The player can introduce the following commands:

* **walk**: Advance to the square the character is facing
* **turn** _left/right_: Turn 90 degrees to the chosen direction
* **use** _element_: Interact with something, like the bow or the exit
* **inventory/inv**: Display the inventory items
* **look around**: Describe elements on your current square
* **look** _element_: Describe an specific element on the ground or in the character's inventory
* **take** _element_: Pick an element from the ground
* **drop** _element_: Leave an inventory item on the ground

And interact with the following elements:

* **arrow**: The ammunition for your **bow**, don't drop it.
* **bow**: A weapon you can fire as long as you have **arrow**s left.
* **gold**: Your main objective is to retrieve this.
* **exit**: You win the game by exiting the forest once you have gold in your inventory.
* **pit**: A bottomless pit, kills you if you enter its square. The character is warned by a sudden breeze when a pit is nearby
* **wumpus**: An eldritch abomination the player must either avoid or kill with the **bow**. Its stink warns the character of its presence.
* **compass**: NOT an original component on the wumpus game, but the whole point of how this project was implemented was to simplify the process of adding new elements and mechanics. Parametrized games only have the "vanilla" wumpus elements, but you will find a **compass** in **wumpus_02.json**.

## Debug Mode

You can make the game draw the map on each turn by adding the "**--debug**" command:

```python wumpus_game.py --debug```

Each game element will be represented as one of the following characters:
* **w**: Wumpus
* **p**: Pit
* **g**: Gold
* **e**: Exit
* **a**: Arrow
* **c**: Compass
* **^**, **<**, **>**, **v**: The Player

## Program Logic

The idea behind this implementation was to create a framework whose logic was disconnected from the wumpus game, so adding or removing elements could be done relatively fast.

Although I love to program I am yet to work as a proper developer, and so some (or all) of the design decisions may be wrong. Some of the program's most relevant elements are:

- **wumpus.py**: Here we have the _main_ and the game's primary loop.
- **/common/utils/functions.py**: Generic help functions that work outside the wumpus' logic.
- **/games**: The program will look for predefined games here.
- **/logs**: Were logs are stored.
- **/common/GameStatus.py**: Class that stores some information on the player status and also triggers the end of the game.
- **/common/Logger.py**: The game logger.
- **/common/map_elements/MapElement.py**: Class that defines the characteristics of any non-player grid element on the game.
- **/common/map_elements/actors/GameActor.py**: Extension of **MapElement** that defines a "living" entity on the map.
- **/common/map_elements/actors/GameItem.py**: Extension of **MapElement** that defines an item the character can pick and drop.


## Unit Tests

Some unit tests have been implemented with the _pytest_ library to cover the functions of the lazily named **common/utils/functions.py** file, although is far from being an acceptable code coverage.

In order for the tests to run execute the following command in the project's root directory:

```pytest -v```