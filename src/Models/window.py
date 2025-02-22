import pygame

class Window: 
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.titleMenu = pygame.Rect(350,100,100,50)
        self.btnPlay = pygame.Rect(350,300,100,50)
        self.btnExit = pygame.Rect(350,355,100,50)
        self.font = pygame.font.Font(None,36)

    def updateWindow(self):
        
        pygame.display.flip()
    
    def getWindow(self):
        
        return self.window

    def renderSurface(self,surface):
         self.window.blit(surface, (0,0))

    def drawBtns(self):

        titleMenu = self.font.render("BATTLESHIP", True, (255, 255, 255))
        rectTitleMenu = titleMenu.get_rect(center=self.titleMenu.center)

        self.window.blit(titleMenu,rectTitleMenu)
        
        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay) 
        pygame.draw.rect(self.window, (0, 0, 255), self.btnExit)
        
        textPlay = self.font.render('PLAY', True, (255, 255, 255))
        textExit = self.font.render('EXIT', True, (255, 255, 255))

        rectPlay = textPlay.get_rect(center=self.btnPlay.center)
        rectExit = textExit.get_rect(center=self.btnExit.center)
        
        self.window.blit(textPlay, rectPlay)
        self.window.blit(textExit, rectExit)

