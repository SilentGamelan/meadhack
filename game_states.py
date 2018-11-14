from enum import Enum


# TODO - upgrade to python 3.6 and use auto() enumerating - remember to import
class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3