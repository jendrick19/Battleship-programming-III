#Si van ejecutar el programa en otro archivo python 
#deben comentar el import que hice acá, o sino les dará error

class Ship:
    def __init__(self, name, size, orientation, position):
        self.name = name
        self.size = size
        self.orientation = orientation
        self.position = position
        self.life = size
    
    def check_sunken_ship(self):
        return self.life == 0
    
    def damage_received_ship(self):
        if self.check_sunken_ship():
            return f"El barco {self.name} ya está hundido."
        self.life -= 1
        return f"El barco {self.name} ha recibido daño."