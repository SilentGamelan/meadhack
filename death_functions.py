import libtcodpy as libtcod

from game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return "You've snuffed it matey", GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} has karked it!'.format(monster.name.capitalize())


    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'The bloody remains of ' + monster.name

    return death_message

