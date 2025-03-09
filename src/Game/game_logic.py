from board import board
from ship import ship

class Game:
    def __init__(self):
        self.board = board()
        #Barco de ejemplo
        self.ships = [ship([(1, 1), (1, 2), (1, 3)])]

    def shoot(self, x, y):
        """Valida y ejecuta un disparo."""
        if not self.board.is_valid_shot(x, y):
            print("Disparo inválido, intenta otra coordenada.")
            return False
        
        hit = any(ship.register_hit(x, y) for ship in self.ships)
        self.board.register_shot(x, y, hit)

        if hit:
            print("¡Impacto!")
        else:
            print("Agua.")

        self.board.display()
        return True