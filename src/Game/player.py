from board import Board
from ship import Ship

class Player:
    def __init__(self, name):
        """Inicializa al jugador """
        self.name = name
        self.board = Board(10)
        self.ships = []
        self.opponent_board = Board(10)  # Tablero para registrar disparos al oponente

    def add_ship(self, ship):
        """Agrega un barco al tablero del jugador si es válido"""
        if ship.place_ship(self.board):
            self.ships.append(ship)
            print(f"El barco {ship.name} se ha añadido correctamente para {self.name}.")
        else:
            print(f"No se pudo colocar el barco {ship.name} para {self.name}.")

    def register_shot(self, row, col):
        """Registra un disparo del oponente en el tablero del jugador"""
        result = self.board.register_shot(row, col)
        if result == "Disparo exitoso":
            for ship in self.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship()
                    break
        print(f"{self.name}: {result}")
        return result

    def shoot_at_opponent(self, opponent, row, col):
        """Dispara al tablero del oponente"""
        result = opponent.register_shot(row, col)
        if result == "Disparo exitoso":
            self.opponent_board.grid[row][col] = 'x'
        elif result == "Disparo fallido":
            self.opponent_board.grid[row][col] = 'o'
        else:
            print(result)  
        return result

    def all_ships_sunken(self):
        """Verifica si todos los barcos del jugador están hundidos"""
        for ship in self.ships:
            if ship.life > 0:
                return False
        print(f"¡Todos los barcos de {self.name} han sido hundidos!")
        return True
