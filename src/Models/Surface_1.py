import pygame

class Surface_1:

    def __init__(self,widthS, heightS):
        pygame.font.init()
        self.widthS=widthS
        self.heightS=heightS
       
        self.btnContinue= pygame.Rect(250,400,120,50)
        self.btnReset= pygame.Rect(250,500,100,50)
       
        self.surface = pygame.Surface((widthS,heightS))
        self.surface.fill((0, 128, 255))
        
        self.gridSz = 10
        self.cellSz = 30
        self.xGrid = self.gridSz*self.cellSz
        self.offset_x, self.offset_y = (self.widthS-self.xGrid)//2,80
        self.gridP = None
        
        self.font = pygame.font.Font(None,24)
        
        
    def create_Player_Grid(self):
        self.gridP= [[' ' for _ in range(self.gridSze)] for _ in range(self.gridSz)]
    
    def drawGrid(self):
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0,0,0), rect, 1)
    
    def updateWindow(self):
        
        pygame.display.flip()
        
    def drawBtn(self):
        pygame.draw.rect(self.surface,(255,0,0), self.btnContinue)
        pygame.draw.rect(self.surface,(255,0,0), self.btnReset)
        
        textContinue=self.font.render('Continue', True, (255, 255, 255))
        textReset=self.font.render('Reset', True, (255, 255, 255))
     
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        rectReset = textReset.get_rect(center=self.btnReset.center)

        self.surface.blit(textContinue, rectContinue)
        self.surface.blit(textReset, rectReset)
        
        
    
            


                 
                
         
