from board import Board
from ship import Ship

class GameLogic:
    def _init_(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        

    def update_sunk_ships (self, is_player):
        if is_player:
         shipSunkens = 0
         ship= ship.check_sunken_ships
        if is_player:
            for ship in self.player1.ships:
                if ship.check_sunken_ship():
                    shipSunkens += 1
            self.player1.shipSunkens = shipSunkens
        else:
            for ship in self.player2.ships:
                if ship.check_sunken_ship():
                    shipSunkens += 1
            self.player2.shipSunkens = shipSunkens

        
    def check_victory (self, is_player):
        if is_player:
         if self.player1.shipSunkens == len (self.player1.ships):
            print("El jugador 2 ha ganado")
            return True
        if self.player2.shipSunkens == len (self.player2.ships):
            print("El jugador 1 ha ganado")
            return True
        else:
            return False

class Game:
    def __init__(self):
        """Inicializa el tablero y coloca los barcos"""
        self.board = Board(10)
        self.ships = [
            Ship('Destructor', 3, 'horizontal', [(2, 3), (2, 4), (2, 5)]),
            Ship('Crucero', 2, 'vertical', [(5, 5), (6, 5)])
        ]
        for ship in self.ships:
            ship.place_ship(self.board)

    #Metodo para los disparos
    def shoot(self, row, col):
        if not (0 <= row < self.board.size and 0 <= col < self.board.size):
            print("Casilla fuera de rango")
            return

        result = self.board.register_shot(row, col)
        print(result)
        self.display_board()



    def display_board(self):
        """Muestra el estado actual del tablero"""
        for row in self.board.board_state():
            print(" ".join(row))
        print()

# Prueba del juego
game = Game()
game.shoot(2, 3)  # Impacto
game.shoot(5, 5)  # Impacto
game.shoot(6, 5)  # ¡Barco hundido!
game.shoot(0, 0)  # Disparo fallido
game.shoot(2, 3)  # Ya se atacó esa casilla
game.shoot(10, 10)  # Casilla fuera de rango
