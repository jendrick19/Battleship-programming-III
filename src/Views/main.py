import sys
import os
import pygame
import time
import logging
from src.Models.window import Window
from src.Models.gameSurface import GameSurface
from src.Link.connection import Conexion
from src.Game.player import Player
from src.Models.ship import Ship

logger = logging.getLogger(__name__)

STATE_SETUP = "setup"
STATE_PLAYING = "playing"
STATE_WAITING = "waiting_for_opponent"
STATE_OVER = "game_over"


def do_initial_handshake(connection, current_surface, titulo, modo_servidor):
    if not connection.connected:
        logger.error("[HANDSHAKE] La conexión no está activa al iniciar handshake.")
        return None
    try:
        barcos_serializados = [
            {"length": s.length, "x": s.x, "y": s.y, "isHorizontal": s.isHorizontal}
            for s in current_surface.ships
        ]
        logger.debug("[HANDSHAKE] Barcos serializados correctamente")

        if modo_servidor:
            logger.debug("[HANDSHAKE] Modo servidor: esperando al cliente...")

            current_surface.status_message = "Esperando barcos del cliente..."
            current_surface.status_timer = pygame.time.get_ticks() + 20000
            data = None
            start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start < 20000:
                msg = connection.get_mensaje()
                if msg and msg.get("type") == "player_ready":
                    logger.debug("[HANDSHAKE] Recibido player_ready del cliente: %s", msg)
                    data = msg
                    break

                current_surface.draw()
                pygame.display.get_surface().blit(current_surface.surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)

            if data:
                logger.debug("[HANDSHAKE] Enviando respuesta player_ready del servidor...")
                connection.enviar_datos({
                    "type": "player_ready",
                    "name": titulo,
                    "ships": barcos_serializados
                })

                current_surface.status_message = "Turno inicial para ti"
                current_surface.status_timer = pygame.time.get_ticks() + 3000
                current_surface.state = "playing"

                logger.debug("[HANDSHAKE] Handshake del servidor completado con éxito.")
                return data
            else:
                logger.warning("[HANDSHAKE] Timeout esperando player_ready del cliente.")
                current_surface.status_message = "Timeout esperando al cliente"
                current_surface.status_timer = pygame.time.get_ticks() + 4000
                return None

        else:
            logger.debug("[HANDSHAKE] Modo cliente: enviando player_ready...")
            connection.enviar_datos({
                "type": "player_ready",
                "name": titulo,
                "ships": barcos_serializados
            })

            current_surface.status_message = "Esperando confirmación del servidor..."
            current_surface.status_timer = pygame.time.get_ticks() + 20000
            data = None
            start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start < 20000:
                msg = connection.get_mensaje()
                if msg and msg.get("type") == "player_ready":
                    logger.debug("[HANDSHAKE] Recibido player_ready del servidor: %s", msg)
                    data = msg
                    break

                current_surface.draw()
                pygame.display.get_surface().blit(current_surface.surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)

            if data:
                current_surface.state = "waiting_for_opponent"
                current_surface.status_message = "Esperando turno inicial del servidor..."
                current_surface.status_timer = pygame.time.get_ticks() + 5000
                logger.debug("[HANDSHAKE] Handshake del cliente completado con éxito.")
                return data
            else:
                logger.warning("[HANDSHAKE] Timeout esperando player_ready del servidor.")
                current_surface.status_message = "Timeout esperando al servidor"
                current_surface.status_timer = pygame.time.get_ticks() + 4000
                return None

    except Exception as e:
        logger.exception("[HANDSHAKE] Error inesperado durante handshake: %s", e)
        current_surface.status_message = f"Error: {e}"
        current_surface.status_timer = pygame.time.get_ticks() + 5000
        return None

def game():
    pygame.init()
    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    modo_servidor = input("¿Eres el servidor? (s/n): ").strip().lower() == 's'
    ip = "0.0.0.0" if modo_servidor else input("Ingresa la IP del servidor: ").strip()
    puerto = 5000

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

    titulo = "Player 1" if modo_servidor else "Player 2"
    color = (119, 255, 148) if modo_servidor else (255, 163, 175)
    current_surface = GameSurface(f"Choose the position of your ships {titulo}", 800, 600, color, connection)
    current_surface.status_message = ""
    current_surface.status_timer = 0

    execute = True
    game_started = False

    while execute:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                execute = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_surface.state == STATE_SETUP:
                    action = current_surface.handle_click(pygame.mouse.get_pos())
                    if action == "continue" and current_surface.setup_player(titulo):
                        logging.debug("[SETUP] Player local configurado correctamente.")
                        logging.debug("[HANDSHAKE] Iniciando handshake con el oponente...")
                        handshake_data = do_initial_handshake(connection, current_surface, titulo, modo_servidor=modo_servidor)
                        logging.debug("[HANDSHAKE] handshake_data recibido: %s", handshake_data)
                        print("[DEBUG handshake] handshake_data =", handshake_data)
                        if handshake_data and handshake_data["type"] == "player_ready":
                            logging.debug("[OPPONENT] Creando oponente: %s", handshake_data["name"])
                            opponent = Player(handshake_data["name"])
                            for s in handshake_data["ships"]:
                                opponent.add_ship(Ship(s["length"], s["x"], s["y"], s["isHorizontal"]))
                            current_surface.setup_opponent(opponent)

                            if modo_servidor:
                                current_surface.switch_to_playing()
                                logging.debug("[TURN] Servidor cambia a PLAYING")
                                connection.enviar_datos({"type": "turn_ready"})
                                logging.debug("[TURN] Servidor envió turn_ready")
                            else:
                                current_surface.state = STATE_WAITING
                                current_surface.status_message = "Esperando turno inicial del servidor..."
                                current_surface.status_timer = pygame.time.get_ticks() + 5000
                            game_started = True
                        else:
                            current_surface.status_message = "Handshake fallido"
                            current_surface.status_timer = pygame.time.get_ticks() + 4000

                elif current_surface.state == STATE_PLAYING:
                    action = current_surface.handle_click(pygame.mouse.get_pos())
                    if action == "end_turn" and not current_surface.game_over:
                        current_surface.end_turn()

                elif current_surface.game_over and current_surface.btnReset.collidepoint(pygame.mouse.get_pos()):
                    connection.finalizar()
                    game()
                    return

        msg = connection.get_mensaje()
        if msg:
            if msg["type"] == "turn_ready":
                logging.debug("[RED] Se recibió turn_ready, cambiando a PLAYING")
                current_surface.switch_to_playing()
            elif msg["type"] == "turn_complete":
                logging.debug("[RED] Se recibió turn_complete, cambiando a PLAYING")
                current_surface.switch_to_playing()
            elif msg["type"] == "victory":
                current_surface.game_over = True
                current_surface.winner = f"Player {msg['winner']}"

        if current_surface:
            if game_started and current_surface.state == STATE_WAITING:
                logging.debug("[WAIT] Ejecutando wait_for_opponent_turn")
                current_surface.wait_for_opponent_turn()
            current_surface.handle_events(events)
            current_surface.draw()
            if hasattr(current_surface, 'status_message') and pygame.time.get_ticks() < current_surface.status_timer:
                font = pygame.font.Font(None, 24)
                text = font.render(current_surface.status_message, True, (255, 255, 0))
                current_surface.surface.blit(text, text.get_rect(center=(400, 570)))
            window.renderSurface(current_surface.surface)
        window.updateWindow()

    connection.finalizar()
    pygame.quit()
    sys.exit()

game()