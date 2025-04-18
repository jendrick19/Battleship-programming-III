import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pygame
from src.Models.window import Window
from src.Models.gameSurface import GameSurface

def game():
    pygame.init()

    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    surfacePlayer1 = GameSurface('Choose the position of your ships player 1', 800, 600, (119, 255, 148))
    surfacePlayer2 = GameSurface('Choose the position of your ships player 2', 800, 600, (255, 163, 175))

    execute = True
    current_surface = None
    game_started = False
    mouse_pos = (0, 0)  # Inicializar mouse_pos

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
                            if current_surface.setup_player("Player 1"):
                                current_surface = surfacePlayer2
                        elif current_surface == surfacePlayer2:
                            if current_surface.setup_player("Player 2"):
                                # Set up opponents
                                surfacePlayer1.setup_opponent(surfacePlayer2.player)
                                surfacePlayer2.setup_opponent(surfacePlayer1.player)
                                
                                # Switch to playing mode
                                surfacePlayer1.switch_to_playing()
                                surfacePlayer2.switch_to_playing()
                                
                                current_surface = surfacePlayer1
                                game_started = True
                    
                    elif action == "end_turn" and current_surface.game_over == False:
                        if current_surface == surfacePlayer1:
                            current_surface = surfacePlayer2
                            surfacePlayer2.reset_shot_flag()
                        else:
                            current_surface = surfacePlayer1
                            surfacePlayer1.reset_shot_flag()
                    
                    # Manejar eventos de movimiento de barcos
                    elif action == "ship_moved":
                        # No es necesario hacer nada especial aquí, solo redibujamos
                        pass

        if current_surface is not None:
            # Verificar si se hizo clic en el botón de reinicio cuando el juego ha terminado
            if hasattr(current_surface, 'game_over') and current_surface.game_over and hasattr(current_surface, 'btnReset'):
                if current_surface.btnReset.collidepoint(mouse_pos):
                    game()
                    return

            current_surface.handle_events(events)
            current_surface.draw()
            window.renderSurface(current_surface.surface)
        else:
            window.drawBtns()

        window.updateWindow()

    pygame.quit()
    sys.exit()

game()