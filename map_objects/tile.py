# tile.py
# Contains the Tile class, which deals with blocking of movement/LOS

class Tile: 
    """
    A Tile on the map - can have the properties of blocking movement/vision
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, if a tile blocks movement, it also blocks vision
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight
