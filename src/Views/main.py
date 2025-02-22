import pygame
from src.Models.window import Window
from src.Models.surface_1 import Surface_1

pygame.init()

window = Window(800,600, 'BATTLESHIP')
window.drawBtns()

surfacePlayer1 = Surface_1(800,600)

execute = True

while execute:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execute = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
               mouse_pos = pygame.mouse.get_pos()
               if window.btnPlay.collidepoint(mouse_pos):
                surfacePlayer1.drawGrid()
                surfacePlayer1.drawBtn()
                window.renderSurface(surfacePlayer1.surface)
                
    window.updateWindow()
