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
STATE_MENU = "menu"  # New state for the main menu


def do_initial_handshake(connection, current_surface, titulo, modo_servidor):
    if not connection.connected:
        logger.error("[HANDSHAKE] The connection is not active when starting handshake.")
        return None
    try:
        barcos_serializados = [
            {"length": s.length, "x": s.x, "y": s.y, "isHorizontal": s.isHorizontal}
            for s in current_surface.ships
        ]
        logger.debug("[HANDSHAKE] Ships serialized correctly")

        if modo_servidor:
            logger.debug("[HANDSHAKE] Server mode: waiting for client...")

            current_surface.status_message = "Waiting for client ships..."
            current_surface.status_timer = pygame.time.get_ticks() + 60000  # Aumentado a 60 segundos
            data = None
            start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start < 60000:  # Aumentado a 60 segundos
                msg = connection.get_mensaje()
                if msg and msg.get("type") == "player_ready":
                    logger.debug("[HANDSHAKE] Received player_ready from client: %s", msg)
                    data = msg
                    break

                current_surface.draw()
                pygame.display.get_surface().blit(current_surface.surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)

            if data:
                logger.debug("[HANDSHAKE] Sending player_ready response from server...")
                connection.enviar_datos({
                    "type": "player_ready",
                    "name": titulo,
                    "ships": barcos_serializados
                })

                # Don't set the state here, it will be done later
                logger.debug("[HANDSHAKE] Server handshake completed successfully.")
                return data
            else:
                logger.warning("[HANDSHAKE] Timeout waiting for player_ready from client.")
                current_surface.status_message = "Timeout waiting for client"
                current_surface.status_timer = pygame.time.get_ticks() + 4000
                return None

        else:
            logger.debug("[HANDSHAKE] Client mode: sending player_ready...")
            connection.enviar_datos({
                "type": "player_ready",
                "name": titulo,
                "ships": barcos_serializados
            })

            current_surface.status_message = "Waiting for server confirmation..."
            current_surface.status_timer = pygame.time.get_ticks() + 60000  # Aumentado a 60 segundos
            data = None
            start = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start < 60000:  # Aumentado a 60 segundos
                msg = connection.get_mensaje()
                if msg and msg.get("type") == "player_ready":
                    logger.debug("[HANDSHAKE] Received player_ready from server: %s", msg)
                    data = msg
                    break

                current_surface.draw()
                pygame.display.get_surface().blit(current_surface.surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)

            if data:
                # Don't set the state here, it will be done later
                logger.debug("[HANDSHAKE] Client handshake completed successfully.")
                return data
            else:
                logger.warning("[HANDSHAKE] Timeout waiting for player_ready from server.")
                current_surface.status_message = "Timeout waiting for server"
                current_surface.status_timer = pygame.time.get_ticks() + 4000
                return None

    except Exception as e:
        logger.exception("[HANDSHAKE] Unexpected error during handshake: %s", e)
        current_surface.status_message = f"Error: {e}"
        current_surface.status_timer = pygame.time.get_ticks() + 5000
        return None


def game():
    pygame.init()
    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    current_state = STATE_MENU
    current_surface = None
    connection = None
    game_started = False
    last_update_time = pygame.time.get_ticks()
    update_interval = 16  # Update every 16ms (~60 FPS) for smoother interaction
    execute = True

    home_btn = pygame.Rect(720, 20, 60, 40)

    while execute:
        # Get all events at once
        events = pygame.event.get()
        
        # --- Process quit events first ---
        for event in events:
            if event.type == pygame.QUIT:
                execute = False
                if connection:
                    connection.finalizar()
                break

        # --- Process global MOUSEBUTTONUP events to ensure dragging state is reset ---
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if current_surface and current_state == STATE_SETUP:
                    # Force end dragging for all ships
                    for ship in current_surface.ships:
                        if ship.dragging:
                            ship.end_drag(current_surface.gridSz, current_surface.ships)
                        # Force reset dragging state
                        ship.dragging = False
                        if hasattr(ship, 'mouse_down_pos'):
                            ship.mouse_down_pos = None
        
        # --- Process mouse clicks ---
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Menu state
                if current_state == STATE_MENU:
                    if window.btnPlay.collidepoint(mouse_pos):
                        # Start new game logic...
                        modo_servidor = input("Are you the server? (y/n): ").strip().lower() == 'y'
                        ip = "0.0.0.0" if modo_servidor else input("Enter the server IP: ").strip()
                        puerto = 5000

                        # Connection attempts...
                        intentos = 3
                        for i in range(intentos):
                            try:
                                connection = Conexion(modo_servidor=modo_servidor, ip=ip, puerto=puerto)
                                break
                            except Exception as e:
                                print(f"[Connection] Failed attempt {i+1}: {e}")
                                time.sleep(2 ** i)
                        else:
                            print("[Connection] Could not establish connection.")
                            continue

                        titulo = "Player 1" if modo_servidor else "Player 2"
                        color = (119, 255, 148) if modo_servidor else (255, 163, 175)
                        current_surface = GameSurface(f"Choose your ship positions {titulo}", 800, 600, color, connection)
                        current_surface.status_message = ""
                        current_surface.status_timer = 0
                        current_state = STATE_SETUP

                    elif window.btnExit.collidepoint(mouse_pos):
                        execute = False

                # Other states
                else:
                    # Home button
                    if home_btn.collidepoint(mouse_pos):
                        if connection:
                            connection.finalizar()
                            connection = None
                        current_state = STATE_MENU
                        current_surface = None
                        game_started = False
                        window.drawBtns()
                        continue

                    # Handle clicks in current surface
                    if current_surface:
                        if current_state == STATE_SETUP:
                            action = current_surface.handle_click(mouse_pos)
                            if action == "continue" and current_surface.setup_player(titulo):
                                # Handshake logic...
                                logging.debug("[SETUP] Local player configured correctly.")
                                handshake_data = do_initial_handshake(connection, current_surface, titulo, modo_servidor)
                                logging.debug("[HANDSHAKE] handshake_data received: %s", handshake_data)
                                if handshake_data and handshake_data["type"] == "player_ready":
                                    # Setup opponent...
                                    opponent = Player(handshake_data["name"])
                                    for s in handshake_data["ships"]:
                                        opponent.add_ship(Ship(s["length"], s["x"], s["y"], s["isHorizontal"]))
                                    current_surface.setup_opponent(opponent)

                                    # Set game state based on server/client
                                    if modo_servidor:
                                        current_surface.state = STATE_PLAYING
                                        current_state = STATE_PLAYING
                                        current_surface.status_message = "Initial turn for you"
                                        current_surface.status_timer = pygame.time.get_ticks() + 3000
                                        connection.enviar_datos({"type": "turn_ready"})
                                    else:
                                        current_surface.state = STATE_WAITING
                                        current_state = STATE_WAITING
                                        current_surface.status_message = "Waiting for server's initial turn..."
                                        current_surface.status_timer = pygame.time.get_ticks() + 5000

                                    game_started = True
                                else:
                                    current_surface.status_message = "Handshake failed"
                                    current_surface.status_timer = pygame.time.get_ticks() + 4000

                        elif current_state == STATE_PLAYING:
                            action = current_surface.handle_click(mouse_pos)
                            if action == "end_turn" and not current_surface.game_over:
                                current_surface.end_turn()
                                current_state = STATE_WAITING
                            elif action == "ship_moved":
                                # Force update to show ship movement immediately
                                current_surface.force_update()

                        elif current_state == STATE_OVER and current_surface.btnReset.collidepoint(mouse_pos):
                            if connection:
                                connection.finalizar()
                                connection = None
                            current_state = STATE_MENU
                            current_surface = None
                            game_started = False
                            window.drawBtns()

        # --- Process network messages ---
        if connection and current_surface:
            msg = connection.get_mensaje()
            if msg:
                logging.debug("[NET] Message received: %s", msg)
                try:
                    if msg.get("type") == "turn_ready" or msg.get("type") == "turn_complete":
                        current_state = STATE_PLAYING
                        current_surface.state = STATE_PLAYING
                    current_surface._procesar_mensaje_red(msg)
                    if current_surface.game_over:
                        current_state = STATE_OVER
                except Exception as e:
                    logging.exception("[NET] Error processing message: %s", e)
                    current_surface.status_message = f"Error: {e}"
                    current_surface.status_timer = pygame.time.get_ticks() + 3000

        # --- Update screen ---
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time >= update_interval:
            last_update_time = current_time

            if current_state == STATE_MENU:
                window.drawBtns()

            elif current_surface:
                if game_started and current_state == STATE_WAITING:
                    current_surface.wait_for_opponent_turn()
                    if current_surface.state == STATE_PLAYING:
                        current_state = STATE_PLAYING
                    elif current_surface.game_over:
                        current_state = STATE_OVER
                else:
                    # Handle events in current surface
                    current_surface.handle_events(events)

                # Draw current surface
                current_surface.draw()
                pygame.display.get_surface().blit(current_surface.surface, (0, 0))

                # Draw home button
                pygame.draw.rect(window.window, (250, 250, 250), home_btn)
                font = pygame.font.Font(None, 24)
                home_text = font.render('Home', True, (0, 0, 0))
                home_text_rect = home_text.get_rect(center=home_btn.center)
                window.window.blit(home_text, home_text_rect)

                pygame.display.flip()

            window.updateWindow()

        # Small delay to reduce CPU usage but keep responsiveness
        pygame.time.wait(5)  # Reduced from 10ms to 5ms for better responsiveness

    # --- Clean exit ---
    if connection:
        connection.finalizar()

    pygame.quit()
    sys.exit()

game()
