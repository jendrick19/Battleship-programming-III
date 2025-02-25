import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
import pygame
from src.Models.window import Window
from src.Models.surface import Surface
from src.Models.playingSurface import playingSurface

pygame.init()

window = Window(800, 600, 'BATTLESHIP')
window.drawBtns()

surfacePlayer1 = Surface('Choose the position of your ships player 1', 800, 600)
surfacePlayer1.create_Player_Grid()
surfacePlayer2 = Surface('Choose the position of your ships player 2', 800, 600)
surfacePlayer2.create_Player_Grid()

windowPlayer1 = playingSurface('Turn player 1', 800, 600)
windowPlayer1.create_Player_Grid()
windowPlayer2 = playingSurface('Turn player 2', 800, 600)
windowPlayer2.create_Player_Grid()

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
                    surfacePlayer1.drawShips()
                    surfacePlayer1.drawBtn()
                    window.renderSurface(surfacePlayer1.surface)

                elif window.btnExit.collidepoint(mouse_pos):
                    execute = False

            elif current_surface == surfacePlayer1:
                if surfacePlayer1.btnContinue.collidepoint(mouse_pos):

                    current_surface = surfacePlayer2
                    surfacePlayer2.drawGrid()
                    surfacePlayer2.drawShips()
                    surfacePlayer2.drawBtn()
                    window.renderSurface(surfacePlayer2.surface)

            elif current_surface == surfacePlayer2:
                if surfacePlayer2.btnContinue.collidepoint(mouse_pos):

                    current_surface = windowPlayer1
                    windowPlayer1.copyGridFrom(surfacePlayer1)
                    windowPlayer1.drawGridPosition()
                    windowPlayer1.drawGridAttack()
                    windowPlayer1.drawBtn()
                    window.renderSurface(windowPlayer1.surface)

            elif current_surface == windowPlayer1:
                if windowPlayer1.btnEndShift.collidepoint(mouse_pos):

                    current_surface = windowPlayer2
                    windowPlayer2.copyGridFrom(surfacePlayer2)
                    windowPlayer2.drawGridPosition()
                    windowPlayer2.drawGridAttack()
                    windowPlayer2.drawBtn()
                    window.renderSurface(windowPlayer2.surface) 

    if current_surface is not None:
        window.renderSurface(current_surface.surface)

    else:
        window.drawBtns()

    window.updateWindow()