import pygame
from src.Models.window import Window
from src.Models.surface import Surface

pygame.init()

window = Window(800, 600, 'BATTLESHIP')
window.drawBtns()

surfacePlayer1 = Surface('Choose the position of your ships player 1', 800, 600)
surfacePlayer2 = Surface('Choose the position of your ships player 2', 800, 600)

execute = True
current_surface = None

while execute:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execute = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if current_surface is None:
                if window.btnPlay.collidepoint(mouse_pos):

                    current_surface = surfacePlayer1
                    surfacePlayer1.drawGrid()
                    surfacePlayer1.drawBtn()
                    window.renderSurface(surfacePlayer1.surface)
                    
                elif window.btnExit.collidepoint(mouse_pos):
                    execute = False

            elif current_surface == surfacePlayer1:
                if surfacePlayer1.btnContinue.collidepoint(mouse_pos):

                    current_surface = surfacePlayer2
                    surfacePlayer2.drawGrid()
                    surfacePlayer2.drawBtn()
                    window.renderSurface(surfacePlayer2.surface)

    if current_surface is not None:
        window.renderSurface(current_surface.surface)

    else:
        window.drawBtns()

    window.updateWindow()