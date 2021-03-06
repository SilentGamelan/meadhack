# game_map.py 

"""
Defines the game map as a 2-d array, performs initalisation, and describes methods for interacting with the map object
The dungeon generation algorithm will default to all blocked tiles, and will "dig out" moveable sections instead
"""
import libtcodpy as libtcod
from random import randint

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    # Initially creates all tiles to be NON-BLOCKING
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                 player, entities, max_monsters_per_room):

        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Randomise room width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # Set a random position for room within map boundaries
            # Again, the -1 values are to take into account wall thickness
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Use helper function for checking rooms
            new_room = Rect(x, y, w, h)
            
            # Check if proposed room overlaps another and discard if so
            # Note the pythonic use of for-else-break
            # "if the loop did NOT break, do THIS"
            # I *think* the difference is that if the break is triggered,
            # it doesn't entirely abandon the loop, but just skips the ELSE
            # in the FOR-ELSE structure
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                # find and store co-ords of room centre
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # start player in 1st room created
                    player.x = new_x
                    player.y = new_y
                else:
                    # create tunnel to connect to previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Randomly choose inital tunnel direction
                    if randint(0, 1) == 0:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                
                self.place_entities(new_room, entities, max_monsters_per_room)

                # add new room to room list
                rooms.append(new_room)
                num_rooms += 1


    def create_room(self, room):
        # Make each tile in rectangle passable
        # The +1 accounts for an impassible wall around the room
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose random location in room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and 
                        entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True)
                
                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False   