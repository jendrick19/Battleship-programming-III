from board import board
from ship import ship

class Game:
    def __init__(self):
        #Prueba tablero
        self.board = board(10)
        #Barco de ejemplo
        self.ships = [ship([(1, 1), (1, 2), (1, 3)])]

    def shoot(self, row, col):
        """Valida y ejecuta un disparo."""
        if not self.board.is_valid_shot(row, col):
            print("Disparo inválido, intenta otra coordenada.")
            return False
        
        hit = any(ship.register_hit(row, col) for ship in self.ships)
        self.board.register_shot(row, col, hit)

        if hit:
            print("¡Impacto!")
        else:
            print("Agua.")

        self.board.display()
        return True