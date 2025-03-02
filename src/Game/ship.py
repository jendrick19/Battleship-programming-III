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
        
    def verify_board(self,board):
        x,y = self.position

        if self.orientation == "horizontal":
            if y + self.size > len(board[0]):
                print("Horizontal limit exceeded")
                return False 
            for i in range(self.size):
                if board[x][y + i] != 0:
                    print("One of the cells horizontally is occupied")
                    return False
        
        elif self.orientation == "vertical":
            if x + self.size > len(board):
                print("Vertical limit exceeded")
                return False
            for i in range(self.size):
                if board[x + i][y] != 0:
                    print("One of the cells vertically is occupied")
                    return False
        
        elif self.orientation == "diagonal":
            if x + self.size > len(board) or y + self.size > len(board[0]):
                print("Diagonal limit exceeded")
                return False
            for i in range(self.size):
                if board[x + i][y+i] != 0:
                    print("One of the cells diagonally is occupied")
                    return False
        
        elif self.orientation != 'horizontal' and self.orientation != 'vertical'and self.orientation != 'diagonal':
            print('You have set the wrong orientation')
            return False

        print(f"The boat has been correctly placed in: {x},{y}")
        return True
    
    def place_ship(self,board):
        x,y = self.position
        
        if self.verify_board(board) == False:
            print("Cannot place boat")
            return False

        if self.orientation == "horizontal":
            for i in range(self.size):
                board[x][y+i] = 1
            
        elif self.orientation == "vertical":
            for i in range(self.size):
                board[x+i][y] = 1
        
        elif self.orientation == "diagonal":
            for i in range(self.size):
                board[x+i][y+i] = 1
        
        print(f"The ship {self.name} has been successfully placed in position {self.position} and orientation {self.orientation}")
        
    
    
print_board(board)
ship = Ship('Submarino',5,'horizontal',[3,2])
prueba_verify_board = ship.place_ship(board)
print(prueba_verify_board)
print_board(board)