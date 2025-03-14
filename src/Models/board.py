class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['w' for _ in range(self.size)] for _ in range(self.size)]
