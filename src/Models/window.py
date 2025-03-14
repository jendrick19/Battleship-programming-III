import pygame

class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.window.fill((0, 128, 255))
        
        self.font = pygame.font.Font(None, 36)
        
        self.btnPlay = pygame.Rect(350, 250, 100, 50)
        self.btnExit = pygame.Rect(350, 350, 100, 50)
        
    def drawBtns(self):
        self.window.fill((0, 128, 255))
        
        title = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.window.blit(title, title_rect)
        
        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay)
        pygame.draw.rect(self.window, (255, 0, 0), self.btnExit)
        
        play_text = self.font.render('Play', True, (255, 255, 255))
        exit_text = self.font.render('Exit', True, (255, 255, 255))
        
        play_rect = play_text.get_rect(center=self.btnPlay.center)
        exit_rect = exit_text.get_rect(center=self.btnExit.center)
        
        self.window.blit(play_text, play_rect)
        self.window.blit(exit_text, exit_rect)
        
    def renderSurface(self, surface):
        self.window.blit(surface, (0, 0))
        
    def updateWindow(self):
        pygame.display.update()


