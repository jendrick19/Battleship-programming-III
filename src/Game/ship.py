#Esto solo es para modo de prueba, luego de haber probado y terminado será eliminado
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))
board_size = 5
board = [[0 for _ in range(board_size)] for _ in range(board_size)]

class Ship:
    def __init__(self,name,size,orientation,position):
        self.name = name
        self.size = size
        self.orientation = orientation
        self.position = position
    
    #Preguntar si debo implementarlo para que el jugador eliga los atributos y pensar como hacerlo    
    def veify_board(self,board):
        x,y = self.position

        if self.orientation == "horizontal":
            if y + self.size > len(board[0]):
                return False 
            for i in range(self.size):
                if board[x][y + i] != 0:
                    return False
        
        elif self.orientation == "vertical":
            if x + self.size > len(board):
                return False
            for i in range(self.size):
                if board[x + i][y] != 0:
                    return False
        
        elif self.orientation == "diagonal":
            if x + self.size > len(board) or y + self.size > len(board[0]):
                return False
            for i in range(self.size):
                if board[x + i][y+i] != 0:
                    return False
        
        elif self.orientation != 'horizontal' and self.orientation != 'vertical'and self.orientation != 'diagonal':
            print('Haz establecido una orientación incorrecta')
            return False

        
        return True
     
print_board(board)
ship = Ship('Submarino',2,'horizontal',[1,1])
prueba_verify_board = ship.veify_board(board)
print(prueba_verify_board)