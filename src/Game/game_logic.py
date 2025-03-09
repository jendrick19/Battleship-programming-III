from board import Board
from ship import Ship

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
