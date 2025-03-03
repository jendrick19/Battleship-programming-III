import pygame
from src.Models.ship import Ship
from src.Game.board import Board

class Surface:
    def __init__(self, title, widthS, heightS):
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
        self.offset_x, self.offset_y = 50, 100
        self.gridP = None

        self.ships = [Ship(4, 0, 0), Ship(3, 0, 2), Ship(2, 0, 4)]
        
        self.font = pygame.font.Font(None, 24)
        
    def create_Player_Grid(self):
        self.gridP = Board(self.gridSz)

    def drawGrid(self):
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
    
    def drawShips(self):
        self.gridP = Board(self.gridSz)
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)
            for i in range(ship.length):
                row = int(ship.y)
                col = int(ship.x + i)
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

    def handle_events(self, events):
        for event in events:
            for ship in self.ships:
                ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz)