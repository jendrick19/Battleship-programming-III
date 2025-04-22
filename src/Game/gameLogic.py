class GameLogic:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def check_victory(self):
        """
        Verifica si hay un ganador
        """
        # Verificar si todos los barcos del jugador 1 están hundidos
        if self.player2.all_ships_sunken():
            return 1  # Jugador 1 gana
        
        # Verificar si todos los barcos del jugador 2 están hundidos
        if self.player1.all_ships_sunken():
            return 2  # Jugador 2 gana
        
        # No hay ganador aún
        return 0