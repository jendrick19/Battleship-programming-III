#Si van ejecutar el programa en otro archivo python 
#deben comentar el import que hice acá, o sino les dará error
from board import Board

class Ship:
    def __init__(self,name,size,orientation,position):
        self.name = name
        self.size = size
        self.orientation = orientation
        self.position = position
        self.life = size
    
    def verify_board(self,board):
        for row, col in self.position:
            if not board.verify_limi(row,col):
                print("The ship exceeds the defined coordinates")
                return False
        print("If space is available")
        return True
        
    def place_ship(self,board):
        if self.verify_board(board):
            board.place_ship(self)
            print(f"Ship {self.name} has been placed in {self.position} with orientation {self.orientation} correctly")
            return True
        else: 
            print(f"ship {self.name} could not be placed")
            return False
        
    def check_sunken_ship(self):
        if self.life == 0:
            print(f"The ship {self.name} is sunken")
            return True
        else:
            print(f"The ship {self.name} is not sunk and has {self.life} lives left.")
            
    def damage_received_ship(self):
        if self.check_sunken_ship == True:
            print(f"the ship {self.name} is sunken")
        else:
            self.life -= 1
            print(f"The ship {self.name} has received damage")  
    
    #Método para imprimir el tablero solo lo usé para ver si todo iba bien
    def print_board(self, board):
        for row in board.grid:
            print(" ".join(row))
        

#Fase de pruebas                      
# Crear un tablero de 10x10
board = Board(10)
# Crear algunos barcos
ship1 = Ship('Submarino1', 3, 'horizontal', [(1, 1), (1, 2), (1, 3)])
ship2 = Ship('Submarino2', 2, 'vertical', [(3, 2), (4, 2)])  
# Colocar los barcos en el tablero
ship1.place_ship(board)
ship2.place_ship(board)
# Imprimir el estado inicial del tablero
print("\nEstado inicial del tablero:")
ship1.print_board(board)
# Verificar el estado de los barcos después de los disparos
ship1.damage_received_ship()  # El barco 1 recibe daño
ship2.damage_received_ship()  # El barco 2 recibe daño
# Verificar si algún barco está hundido
ship1.check_sunken_ship()
ship2.check_sunken_ship()
# Imprimir el estado del tablero después de los disparos
print("\nEstado del tablero después de los disparos:")
ship1.print_board(board)