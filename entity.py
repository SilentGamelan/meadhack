class Entity:
    '''
    A generic object to represent player, enemies, items
    '''
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    
    def move(self, dx, dy):
        # move the entity by a given vector
        self.x += dx
        self.y += dy
        