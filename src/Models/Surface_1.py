import pygame

class Surface_1:
        
    def __init__(self,widthS, heightS):
        pygame.font.init()
        self.widthS=widthS
        self.heightS=heightS
        #######################
        self.btnContinue= pygame.Rect(400,600,130,50)
        self.btnReset= pygame.Rect(250,600,130,50)
        #################################################
        self.surface1= pygame.Surface((widthS,heightS))
        self.surface1.fill((0, 128, 255))
        ####################################
        self.gridSz=10
        self.cellSz=40
        self.xGrid=self.gridSz*self.cellSz
        self.offset_x, self.offset_y=(self.widthS-self.xGrid)//2,120
        self.gridP=None
        ########################
        self.font=pygame.font.Font(None,36)
        
        
    def create_Player_Grid(self):
        self.gridP= [[' ' for _ in range(self.gridSze)] for _ in range(self.gridSz)]
    
    def drawGrid(self):
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface1, (0,0,0), rect, 1)  # Dibuja el borde de la celda
    
    def updateWindow(self):
        
        pygame.display.flip()
        
    def drawBtn(self):
        pygame.draw.rect(self.surface1,(255,0,0), self.btnContinue)
        pygame.draw.rect(self.surface1,(255,0,0), self.btnReset)
        
        textContinue=self.font.render('Continue', True, (255, 255, 255))
        textReset=self.font.render('Reset', True, (255, 255, 255))
     
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        rectReset = textReset.get_rect(center=self.btnReset.center)

        self.surface1.blit(textContinue, rectContinue)
        self.surface1.blit(textReset, rectReset)
        
        
    
            


                 
                
         
