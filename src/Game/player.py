from board import Board
from ship import Ship

class Player:
    def __init__(self, name):
        """Inicializa al jugador con su nombre, tablero y barcos."""
        self.name = name
        self.board = Board(10)  # Tablero propio del jugador
        self.opponent_board = Board(10)  # Tablero para registrar disparos al oponente
        self.ships = []  # Lista de barcos del jugador

    def add_ship(self, ship):
        """Agrega un barco al tablero del jugador si es válido."""
        if self.board.place_ship(ship):  
            self.ships.append(ship)
            print(f"El barco {ship.name} se ha añadido correctamente para {self.name}.")
        else:
            print(f"No se pudo colocar el barco {ship.name} para {self.name}.")

    def shoot_at_opponent(self, opponent, row, col):
        """Dispara al tablero del oponente."""
        result = opponent.board.register_shot(row, col)  # Registrar disparo en el tablero del oponente
        
        # Actualizar el tablero local del jugador que dispara (opponent_board)
        if result == "Disparo exitoso":
            self.opponent_board.grid[row][col] = 'x'  
        elif result == "Disparo fallido":
            self.opponent_board.grid[row][col] = 'o'  

        # Mostrar resultado del disparo
        print(f"{self.name} disparó a ({row}, {col}): {result}")
        return result

    def all_ships_sunken(self):
        """Verifica si todos los barcos del jugador están hundidos."""
        all_sunken = all(ship.life == 0 for ship in self.ships)
        if all_sunken:
            print(f"¡Todos los barcos de {self.name} han sido hundidos!")
        return all_sunken


