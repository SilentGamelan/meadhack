
import libtcodpy as libtcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        # Attacks if adjacent, tries to use A* pathing in entity and basic pathing if cannot
        # move_astar() will call move_towards() if path blocked [both in entity.py] 
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                print('The {0} says something crude about your mother. Your pride is damaged!'.format(monster.name))
