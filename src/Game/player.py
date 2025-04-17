from src.Models.board import Board
from src.Models.ship import Ship

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)
        self.ships = []
    
    def add_ship(self, ship):
        self.ships.append(ship)
        for row, col in ship.position:
            if 0 <= row < self.board.size and 0 <= col < self.board.size:
                self.board.grid[row][col] = 's'
    
    def shoot_at_opponent(self, opponent, row, col):
      
        result = "Disparo fallido"
        
        if opponent.board.grid[row][col] == 's':
            opponent.board.grid[row][col] = 'x'
            result = "Disparo exitoso"
            
            for ship in opponent.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship(row,col)
                    break
        else:
            opponent.board.grid[row][col] = 'o'
        
        return result
    
    def all_ships_sunken(self):
        return all(ship.check_sunken_ship() for ship in self.ships)


