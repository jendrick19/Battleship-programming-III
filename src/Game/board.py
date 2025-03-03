#from ship import Ship

class Board:
    size = 10
    def __init__(self,size):
        self.size=size
        self.grid = [['w' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []

    def verify_limi(self,row,col):
        return 0 <= row <= self.size and 0 <= col <= self.size
    
    def verify_space(self,ship): 
        for row, col in ship.position:
            if not self.verify_limi(row, col) or self.grid[row][col] != 'w':
                return False
        return True

    def place_ship(self,ship):
        if self.verify_space(ship):
            for row, col in ship.position:
                self.grid[row][col] = 's'
            self.ships.append(ship)
            return True
        return False
    
    def register_shot(self,row,col):

        if not self.verify_limi(row,col):
            return "Casilla fuera de rango de disparo"
       
        if self.grid[row][col] == 's':
            self.grid[row][col] = 'x'
            return "Disparo exitoso"

        elif self.grid[row][col] == 'w':
            self.grid[row][col] = 'o'
            return "Disparo fallido"
        
        
        return "Ya se ataco esa casilla"

    def board_state(self):
        return [['x'if esp=='x' else 'o' if esp=='o' else 'w' for esp in row] for row in self.grid]
    

"""Pruebas del tablero
t= Board(10)
#Imprimo tamaño del tablero
print(t.size)
#Verifico diferentes disparos en el tablero, fuera de los limites y dentro de ellos
print(t.verify_limi(10,11))
print(t.register_shot(1,1))
print(t.register_shot(1,12))
print(t.register_shot(1,1))
#Verifico si registra un impacto a una casilla en donde señala hay un barco
t.grid[1][2]="s"
print(t.register_shot(1,2))
print(t.register_shot(1,2))
#Imprimo el estado del tablero
print (t.board_state)"""