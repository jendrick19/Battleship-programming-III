import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pygame
from src.Models.window import Window
from src.Models.gameSurface import GameSurface

pygame.init()

window = Window(800, 600, 'BATTLESHIP')
window.drawBtns()

surfacePlayer1 = GameSurface('Choose the position of your ships player 1', 800, 600)
surfacePlayer2 = GameSurface('Choose the position of your ships player 2', 800, 600)

execute = True
current_surface = None
game_started = False

while execute:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            execute = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if current_surface is None:
                if window.btnPlay.collidepoint(mouse_pos):
                    current_surface = surfacePlayer1
                    current_surface.draw()
                    window.renderSurface(current_surface.surface)

                elif window.btnExit.collidepoint(mouse_pos):
                    execute = False

            else:
                action = current_surface.handle_click(mouse_pos)
                
                if action == "continue":
                    if current_surface == surfacePlayer1:
                        surfacePlayer1.setup_player("Player 1")
                        current_surface = surfacePlayer2
                    elif current_surface == surfacePlayer2:
                        surfacePlayer2.setup_player("Player 2")
                        
                        # Set up opponents
                        surfacePlayer1.setup_opponent(surfacePlayer2.player)
                        surfacePlayer2.setup_opponent(surfacePlayer1.player)
                        
                        # Switch to playing mode
                        surfacePlayer1.switch_to_playing()
                        surfacePlayer2.switch_to_playing()
                        
                        current_surface = surfacePlayer1
                        game_started = True
                
                elif action == "reset":
                    if current_surface == surfacePlayer1:
                        surfacePlayer1 = GameSurface('Choose the position of your ships player 1', 800, 600)
                        current_surface = surfacePlayer1
                    elif current_surface == surfacePlayer2:
                        surfacePlayer2 = GameSurface('Choose the position of your ships player 2', 800, 600)
                        current_surface = surfacePlayer2
                
                elif action == "end_turn":
                    if current_surface == surfacePlayer1:
                        current_surface = surfacePlayer2
                        surfacePlayer2.reset_shot_flag()
                    else:
                        current_surface = surfacePlayer1
                        surfacePlayer1.reset_shot_flag()

    if current_surface is not None:
        current_surface.handle_events(events)
        current_surface.draw()
        window.renderSurface(current_surface.surface)
    else:
        window.drawBtns()

    window.updateWindow()

pygame.quit()
sys.exit()
