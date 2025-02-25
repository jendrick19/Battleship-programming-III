class Ship: 
    def __init__(self, length, x, y):
        self.length = length
        self.x = x
        self.y = y
        self.hits = 0
        self.sunk = False

    