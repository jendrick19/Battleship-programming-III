import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pygame
from src.Models.window import Window
from src.Models.gameSurface import GameSurface
from src.Link.connection import Conexion
from src.Game.player import Player
from src.Models.ship import Ship

def game():
    pygame.init()
    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    modo_servidor = input("¿Eres el servidor? (s/n): ").strip().lower() == 's'

    if modo_servidor:
        ip = "0.0.0.0"
    else:
        ip = input("Ingresa la IP del servidor: ").strip()

    puerto = 5000
    connection = Conexion(modo_servidor=modo_servidor, ip=ip, puerto=puerto)

    titulo = "Player 1" if modo_servidor else "Player 2"
    color = (119, 255, 148) if modo_servidor else (255, 163, 175)
    current_surface = GameSurface(f"Choose the position of your ships {titulo}", 800, 600, color, connection)

    # NUEVO: status_message para mensajes temporales
    current_surface.status_message = ""
    current_surface.status_timer = 0

    execute = True
    game_started = False
    mouse_pos = (0, 0)

    while execute:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                execute = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if current_surface.state == "setup":
                    action = current_surface.handle_click(mouse_pos)

                    if action == "continue":
                        if current_surface.setup_player(titulo):
                            # 1. Enviar mis barcos al oponente
                            barcos_serializados = [
                                {
                                    "length": s.length,
                                    "x": s.x,
                                    "y": s.y,
                                    "isHorizontal": s.isHorizontal
                                } for s in current_surface.ships
                            ]
                            connection.enviar_datos({
                                "type": "player_ready",
                                "name": titulo,
                                "ships": barcos_serializados
                            })

                            # 2. Recibir barcos del oponente
                            data = connection.recibir_datos()
                            if data and data["type"] == "player_ready":
                                opponent_player = Player(data["name"])
                                for ship_data in data["ships"]:
                                    ship = Ship(
                                        ship_data["length"],
                                        ship_data["x"],
                                        ship_data["y"],
                                        ship_data["isHorizontal"]
                                    )
                                    opponent_player.add_ship(ship)

                                current_surface.setup_opponent(opponent_player)
                                current_surface.switch_to_playing()

                                if modo_servidor:
                                    connection.enviar_datos({
                                        "type": "turn_ready"
                                    })
                                else:
                                    current_surface.state = "waiting_for_opponent"
                                    current_surface.status_message = "Esperando turno inicial del servidor..."
                                    current_surface.status_timer = pygame.time.get_ticks() + 5000

                                game_started = True

                elif current_surface.state == "playing":
                    action = current_surface.handle_click(mouse_pos)
                    if action == "end_turn" and not current_surface.game_over:
                        current_surface.end_turn()

                elif current_surface.game_over and current_surface.btnReset.collidepoint(mouse_pos):
                    game()
                    return

        if current_surface is not None:
            if game_started and current_surface.state == "waiting_for_opponent":
                current_surface.wait_for_opponent_turn()

            current_surface.handle_events(events)
            current_surface.draw()

            # Dibujar mensaje de estado si existe
            if hasattr(current_surface, 'status_message') and pygame.time.get_ticks() < current_surface.status_timer:
                font = pygame.font.Font(None, 24)
                text = font.render(current_surface.status_message, True, (255, 255, 0))
                rect = text.get_rect(center=(400, 570))
                current_surface.surface.blit(text, rect)

            window.renderSurface(current_surface.surface)
        else:
            window.drawBtns()

        window.updateWindow()

    pygame.quit()
    sys.exit()

game()
