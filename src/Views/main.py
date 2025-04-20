import sys
import os
import pygame
import time
from src.Models.window import Window
from src.Models.gameSurface import GameSurface
from src.Link.connection import Conexion
from src.Game.player import Player
from src.Models.ship import Ship

# Estados del juego
STATE_SETUP = "setup"
STATE_PLAYING = "playing"
STATE_WAITING = "waiting_for_opponent"
STATE_OVER = "game_over"

def do_initial_handshake(connection, current_surface, titulo):
    try:
        # Enviar mis barcos
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

        # Esperar al oponente sin bloquear la UI
        current_surface.status_message = "Esperando barcos del oponente..."
        current_surface.status_timer = pygame.time.get_ticks() + 5000
        data = None
        start = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start < 5000 and not data:
            data = connection.get_mensaje()
            current_surface.draw()
            pygame.display.get_surface().blit(current_surface.surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(100)

        return data

    except Exception as e:
        current_surface.status_message = f"Error: {e}"
        current_surface.status_timer = pygame.time.get_ticks() + 5000
        return None


def game():
    pygame.init()
    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    # === INPUTS DE CONSOLA ===
    modo_servidor = input("¿Eres el servidor? (s/n): ").strip().lower() == 's'
    ip = "0.0.0.0" if modo_servidor else input("Ingresa la IP del servidor: ").strip()
    puerto = 5000

    # Intentar conexión con reintento (cliente)
    intentos = 3
    for i in range(intentos):
        try:
            connection = Conexion(modo_servidor=modo_servidor, ip=ip, puerto=puerto)
            break
        except Exception as e:
            print(f"[Conexión] Fallo intento {i+1}: {e}")
            time.sleep(2 ** i)
    else:
        print("[Conexión] No se pudo establecer conexión.")
        return

    # Inicializar la interfaz de juego
    titulo = "Player 1" if modo_servidor else "Player 2"
    color = (119, 255, 148) if modo_servidor else (255, 163, 175)
    current_surface = GameSurface(f"Choose the position of your ships {titulo}", 800, 600, color, connection)
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

                if current_surface.state == STATE_SETUP:
                    action = current_surface.handle_click(mouse_pos)
                    if action == "continue" and current_surface.setup_player(titulo):
                        handshake_data = do_initial_handshake(connection, current_surface, titulo)

                        if handshake_data and handshake_data["type"] == "player_ready":
                            opponent_player = Player(handshake_data["name"])
                            for ship_data in handshake_data["ships"]:
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
                                connection.enviar_datos({"type": "turn_ready"})
                            else:
                                current_surface.state = STATE_WAITING
                                current_surface.status_message = "Esperando turno inicial del servidor..."
                                current_surface.status_timer = pygame.time.get_ticks() + 5000

                            game_started = True
                        else:
                            current_surface.status_message = "Handshake fallido"
                            current_surface.status_timer = pygame.time.get_ticks() + 4000

                elif current_surface.state == STATE_PLAYING:
                    action = current_surface.handle_click(mouse_pos)
                    if action == "end_turn" and not current_surface.game_over:
                        current_surface.end_turn()

                elif current_surface.game_over and current_surface.btnReset.collidepoint(mouse_pos):
                    connection.finalizar()
                    game()
                    return

        # Procesar mensajes de red cada frame
        msg = connection.get_mensaje()
        if msg:
            if msg["type"] == "turn_ready":
                current_surface.state = STATE_PLAYING
            elif msg["type"] == "victory":
                current_surface.game_over = True
                current_surface.winner = f"Player {msg['winner']}"

        if current_surface is not None:
            if game_started and current_surface.state == STATE_WAITING:
                current_surface.wait_for_opponent_turn()

            current_surface.handle_events(events)
            current_surface.draw()

            if hasattr(current_surface, 'status_message') and pygame.time.get_ticks() < current_surface.status_timer:
                font = pygame.font.Font(None, 24)
                text = font.render(current_surface.status_message, True, (255, 255, 0))
                rect = text.get_rect(center=(400, 570))
                current_surface.surface.blit(text, rect)

            window.renderSurface(current_surface.surface)
        else:
            window.drawBtns()

        window.updateWindow()

    connection.finalizar()
    pygame.quit()
    sys.exit()

game()
