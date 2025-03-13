from ship import Ship

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['w' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
    
    def verify_limi(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size
    
    def verify_space(self, ship): 
        for row, col in ship.position:
            if not self.verify_limi(row, col) or self.grid[row][col] != 'w':
                return False
        return True
    
    def place_ship(self, ship):
        if self.verify_space(ship):
            for row, col in ship.position:
                self.grid[row][col] = 's'
            self.ships.append(ship)
            return True
        return False
    
    def register_shot(self, row, col):
        if not self.verify_limi(row, col):
            return "Casilla fuera de rango de disparo"
        
        if self.grid[row][col] == 's':
            self.grid[row][col] = 'x'
            return "Disparo exitoso"
        
        elif self.grid[row][col] == 'w':
            self.grid[row][col] = 'o'
            return "Disparo fallido"
        
        return "Pilas ya se atacó esa casilla pana"
    
    
    def board_state(self):
        return [[cell for cell in row] for row in self.grid]
    
    
    def display_board(self, show_ships=False):
        print("  " + " ".join(str(i) for i in range(self.size)))  # Encabezado de columnas
        for i, row in enumerate(self.grid):
            if show_ships:
                print(i, " ".join(cell if cell != 's' or show_ships else 'w' for cell in row))
            else:
                print(i, " ".join('w' if cell == 's' else cell for cell in row))