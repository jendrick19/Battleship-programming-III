from game_logic import GameLogic

class TurnManager:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        self.game_logic = GameLogic(player1, player2)
    
    def switch_turn(self):
        self.current_player = 1 - self.current_player
    
    def play_turn(self):
        player = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]
        
        print(f"Turno de {player.name}")
        print("Tu tablero:")
        player.board.display_board(True)  
        print("\nTablero de ataques:")
        opponent.board.display_board(False)  

        row = int(input("Ingrese fila: "))
        col = int(input("Ingrese columna: "))
        
        result = player.shoot_at_opponent(opponent, row, col)
        print(result)
        
        victory_message = self.game_logic.check_victory()
        if victory_message:
            print(victory_message)
            return True
        
        self.switch_turn()
        return False