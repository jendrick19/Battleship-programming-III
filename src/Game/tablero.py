class tablero:
    tama = 10
    def __init__(self,tama):
        self.tama=tama
        self.matriz = [['w' for _ in range(self.tama)] for _ in range(self.tama)]
        self.barcos = []

    def verificar_limi(self,fil,col):
        return 0 <= fil < self.tama and 0 <= col < self.tama
    
    ##def verificar_espacio(self,barco): 
    # metodo para verificar si se puede colocar el barco en espera el desarrollo de la clase barco
    #     for fil, col in barco.posicion:
    #         if not self.verificar_limi(fil, col) or self.matriz[fil][col] != 'w':
    #             return False
    #     return True

    def colocar_barco(self,barco):
        if self.verificar_espacio(barco):
            for fil, col in barco.posicion:
                self.matriz[fil][col] = 'b'
            self.barcos.append(barco)
            return True
        return False
    
    def registrar_disparo(self,fil,col):
       
        if self.matriz[fil][col] == 'b':
            self.matriz[fil][col] = 'x'
            return "Disparo exitoso"
        
        elif self.matriz[fil][col] == 'w':
            self.matriz[fil][col] = 'o'
            return "Disparo fallido"
        
        if not self.verificar_limi(fil,col):
            return "Casilla fuera de rango de disparo"
        
        return "Ya se ataco esa casilla"

    def estado(self):
        return [['x'if esp=='x' else 'o' if esp=='o' else 'w' for esp in fil] for fil in self.matriz]
