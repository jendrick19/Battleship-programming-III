import pygame
from src.Models.ship import Ship

class Surface:
    def __init__(self, title, widthS, heightS, offset_x, offset_y):
        pygame.font.init()
        self.widthS = widthS
        self.heightS = heightS
        self.title = title

        self.titleSurface = pygame.Rect(350, 25, 100, 50)
        self.btnContinue = pygame.Rect(250, 545, 90, 50)
        self.btnReset = pygame.Rect(490, 545, 60, 50)
       
        self.surface = pygame.Surface((widthS, heightS))
        self.surface.fill((0, 128, 255))
        
        self.gridSz = 10
        self.cellSz = 30
        self.xGrid = self.gridSz * self.cellSz
        self.offset_x = offset_x
        self.offset_y= offset_y
        self.gridP = None

        self.ships = [Ship(4, 0, 0, True), Ship(3, 0, 2, True), Ship(2, 0, 4, True)]
        
        self.font = pygame.font.Font(None, 24)
        
    def create_Player_Grid(self):
        self.gridP = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]

    def drawGrid(self):
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
    
    def drawShips(self):
        self.gridP = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)
            
            if ship.isHorizontal:
                for i in range(ship.length):
                    row = int(ship.y)
                    col = int(ship.x + i)
                    if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
                        self.gridP[row][col] = 'S'
            else:
                for i in range(ship.length):
                    row = int(ship.y + i)
                    col = int(ship.x)
                    if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
                        self.gridP[row][col] = 'S'
    
    def updateWindow(self):
        pygame.display.flip()
        
    def drawBtn(self):
        title = self.font.render(self.title, True, (255, 255, 255))
        rectTitle = title.get_rect(center=self.titleSurface.center)
        self.surface.blit(title, rectTitle)

        pygame.draw.rect(self.surface, (255, 0, 0), self.btnContinue)
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset)
        
        textContinue = self.font.render('Continue', True, (255, 255, 255))
        textReset = self.font.render('Reset', True, (255, 255, 255))
     
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        rectReset = textReset.get_rect(center=self.btnReset.center)

        self.surface.blit(textContinue, rectContinue)
        self.surface.blit(textReset, rectReset)
        
        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

    def handle_events(self, events):
        for event in events:
            for ship in self.ships:
                ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz)