import pygame

class playingSurface:

    def __init__(self, title, widthS, heightS):
        pygame.font.init()
        self.widthS = widthS
        self.heightS = heightS
        self.title = title

        self.titleSurface = pygame.Rect(350, 25, 100, 50)
        self.btnEndTurn = pygame.Rect(250, 545, 90, 50)

        self.surface = pygame.Surface((widthS, heightS))
        self.surface.fill((0, 128, 255))

        self.gridSz = 10
        self.cellSz = 30
        self.xGrid = self.gridSz * self.cellSz
        self.offset_x1, self.offset_y1 = 50, 100  
        self.offset_x2, self.offset_y2 = 450, 100 
        self.gridP = None
        self.gridA = None

        self.font = pygame.font.Font(None, 24)

        self.titlePosit_rect = pygame.Rect(self.offset_x1, self.offset_y1 - 40, 200, 50)
        self.titleAttck_rect = pygame.Rect(self.offset_x2, self.offset_y2 - 40, 200, 50)

    def create_Player_Grid(self):
        self.gridP = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]
        self.gridA = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]
    
    def copyGridFrom(self, surface):
        if surface.gridP:
            self.gridP = [row[:] for row in surface.gridP]

    def drawGridPosition(self):
        titlePosit = self.font.render('POSITIONS', True, (0, 0, 0))
        rectTitlePosit = self.titlePosit_rect

        self.surface.blit(titlePosit, rectTitlePosit)

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

                if self.gridP and self.gridP[row][col] == 'S':  
                    pygame.draw.rect(self.surface, (255, 0, 0), rect) 

   
    def drawGridAttack(self):
        titleAttck = self.font.render('ATTACK', True, (0, 0, 0))
        rectTitleAttck = self.titleAttck_rect

        self.surface.blit(titleAttck, rectTitleAttck)

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

    def updateWindow(self):
        pygame.display.flip()

    def drawBtn(self):
        title = self.font.render(self.title, True, (255, 255, 255))
        rectTitle = title.get_rect(center=self.titleSurface.center)

        self.surface.blit(title, rectTitle)

        pygame.draw.rect(self.surface, (255, 0, 0), self.btnEndTurn)

        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))

        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)

        self.surface.blit(textEndTurn, rectEndTurn)