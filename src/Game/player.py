from src.Models.board import Board
from src.Models.ship import Ship

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)
        self.ships = []
        self.damaged_positions = set()  # Conjunto para rastrear posiciones dañadas
        self.hits = []  # Posiciones donde el jugador ha acertado
        self.misses = []  # Posiciones donde el jugador ha fallado
    
    def add_ship(self, ship):
        self.ships.append(ship)
        for row, col in ship.position:
            if 0 <= row < self.board.size and 0 <= col < self.board.size:
                self.board.grid[row][col] = 's'
    
    def shoot_at_opponent(self, opponent, row, col):
        result = "Disparo fallido"
        
        # Verificar si hay un barco en la posición
        if opponent.board.grid[row][col] == 's':
            opponent.board.grid[row][col] = 'x'  # Marcar como golpe
            result = "Disparo exitoso"
            
            # Registrar el acierto
            self.hits.append((row, col))
            
            # Buscar el barco que fue golpeado y dañarlo
            for ship in opponent.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship(row, col)
                    # Añadir a las posiciones dañadas
                    opponent.damaged_positions.add((row, col))
                    break
        else:
            # Marcar como fallo
            opponent.board.grid[row][col] = 'o'
            # Registrar el fallo
            self.misses.append((row, col))
        
        return result
    
    def all_ships_sunken(self):
        """
        Verifica si todos los barcos del jugador han sido hundidos
        """
        for ship in self.ships:
            # Verificar si alguna posición del barco aún tiene 's' (no ha sido golpeada)
            for pos in ship.position:
                row, col = pos
                if self.board.grid[row][col] == 's':
                    # Si al menos una posición no ha sido golpeada, el barco no está hundido
                    return False
        
        # Si llegamos aquí, todos los barcos están hundidos
        return True