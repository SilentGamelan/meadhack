class Entity:
    '''
    A generic object to represent player, enemies, items
    '''
    def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
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


# Note this assumes only one entity per tile
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    
    return None