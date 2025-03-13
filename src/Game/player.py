from board import Board
from ship import Ship

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)
        self.opponent_board = Board(10)
        self.ships = []
    
    def add_ship(self, ship):
        if self.board.place_ship(ship):
            self.ships.append(ship)
    
    def shoot_at_opponent(self, opponent, row, col):
        result = opponent.board.register_shot(row, col)
        
        if result == "Disparo exitoso":
            for ship in opponent.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship()
                    break
        
        return result
    
    def all_ships_sunken(self):
        return all(ship.check_sunken_ship() for ship in self.ships)
