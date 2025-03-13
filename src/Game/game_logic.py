from player import Player

class GameLogic:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def check_victory(self):
        if self.player1.all_ships_sunken():
            return f"{self.player2.name} gano"
        if self.player2.all_ships_sunken():
            return f"{self.player1.name} gano"
        return None