
import libtcodpy as libtcod
import math
from render_functions import RenderOrder

class Entity:
    '''
    A generic object to represent player, enemies, items
    '''
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        

        # setting owner property to self simplifies accessing Entity properties 
        # from within components package
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self
    
    def move(self, dx, dy):
        # move the entity by a given vector
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        # TODO - rewrite so can use distance_to?
        # would require making target object, with .x and .y properties
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or 
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map matching game_map dimensions
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, 
                                           not game_map.tiles[x1][y1].blocked)
        
        # Scan entitites to determine if any objects to navigate around
        # self/target checks to ensure start/end points are free
        # AI module will handle when self and target are adjacent, and will not call move_astar()
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Setting tile as wall (unwalkable) on fov map forces navigation around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)
                        
        # Allocate an A* path
        # 1.41 is the normal diagonal cost of movement, set to 0.0 if prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path beween self and target co-ords
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if valid path exists, limit pathsize to 25 tiles
        # Prevents odd monster behaviour when finding alt routes to player
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find co-ords of next step in path
            x, y = libtcod.path_walk(my_path, True)
            # If both coords exist (ie; the step is traversible), move self to next step
            if x or y:
                self.x = x
                self.y = y
        else:
            # Keep old move function as backup, so if no paths (ie monster blocking corridor)
            # monsters will stil try to move closer to player
            self.move_towards(target.x, target.y, game_map, entities)
    
        # delete path to save memory
        libtcod.path_delete(my_path)


    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)



# Note this assumes only one entity per tile
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    
    return None