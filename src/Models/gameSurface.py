import pygame
import logging
import json
import os
import select
import time
from src.Models.board import Board
from src.Game.player import Player
from src.Game.gameLogic import GameLogic
from src.Models.ship import Ship

logger = logging.getLogger(__name__)

class GameSurface:
    def __init__(self, title, width, height, colorT, connection=None):
        pygame.font.init()
        self.width = width
        self.height = height
        self.title = title
        self.surface = pygame.Surface((width, height))
        self.surface.fill((3, 37, 108))
        self.colorT=colorT
        self.gridSz = 10
        self.cellSz = 30
        self.offset_x = 250
        self.offset_y = 100
        self.last_result_message = ""
        self.last_result_time = 0
        ruta_imagen = os.path.join(os.path.dirname(__file__), '..', '..', '6292.jpg')
        self.backSur = pygame.image.load(os.path.abspath(ruta_imagen))
        self.backSur = pygame.transform.scale(self.backSur, (self.width, self.height))
        self.font_tittle= pygame.font.Font(None, 36)
        self.show_confirmation = False
        self.connection = connection  # Conexion por socket
        self._recv_buffer = ""
        self.status_message = ""
        self.status_timer = 0
        self.red_intentos = 0
        self.status_color = (255, 255, 255)  # Blanco como valor por defecto


        # For playing phase
        self.offset_x1, self.offset_y1 = 50, 100  # Position grid
        self.offset_x2, self.offset_y2 = 450, 100  # Attack grid

        self.font = pygame.font.Font(None, 24)

        # State tracking
        self.state = "setup"  # "setup" or "playing"
        self.player_number = 0
        if "player 1" in title.lower():
            self.player_number = 1
        elif "player 2" in title.lower():
            self.player_number = 2

        # Buttons
        self.btnContinue = pygame.Rect((self.width - 90) // 2, 500, 90, 50)
        self.btnReset = pygame.Rect(340, 400, 120, 50)
        self.btnEndTurn = pygame.Rect((self.width - 90) // 2, 500, 90, 50)
        self.btnConfirmYes = pygame.Rect((self.width - 200) // 2 - 40, 300, 80, 40)
        self.btnConfirmNo = pygame.Rect((self.width - 200) // 2 + 100, 300, 80, 40)

        # Ships for setup
        self.ships = []
        if self.state == "setup":
            self.ships = [
                Ship(4, 0, 0, True),
                Ship(3, 0, 2, True),
                Ship(2, 0, 4, True),
                Ship(2, 0, 6, True),
                Ship(1, 0, 8, True)
            ]

        # Game objects
        self.player = None
        self.opponent = None
        self.game_logic = None

        # UI tracking
        self.hits = []
        self.misses = []
        self.shot_made = False
        self.game_over = False
        self.winner = None

        self.collision_message = ""
        self.message_timer = 0

    def setup_player(self, name):
        if self.has_ship_collisions():
            return False

        self.player = Player(name)
        for ship in self.ships:
            ship.update_positions()
            game_ship = Ship(
                ship.length,
                ship.x,
                ship.y,
                ship.isHorizontal,
                f"Ship{ship.length}"
            )
            self.player.add_ship(game_ship)
        return True

    def setup_opponent(self, opponent):
        self.opponent = opponent
        self.game_logic = GameLogic(self.player, self.opponent)

    def switch_to_playing(self):
        self.state = "playing"
        self.shot_made = False
        self.status_message = "Es tu turno"
        self.status_timer = pygame.time.get_ticks() + 3000


    def has_ship_collisions(self):
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i+1:]:
                if ship1.check_collision([ship2]):
                    return True
        return False

    def draw(self):
        self.surface.fill((3, 37, 108))
        self.surface.blit(self.backSur, (0, 0))

        title = self.font_tittle.render(self.title, True, self.colorT)
        self.surface.blit(title, title.get_rect(center=(self.width // 2, 45)))

        if self.game_over:
            self.draw_game_over()
        elif self.state == "setup":
            self.draw_setup()
        else:
            self.draw_playing()

        # Mostrar mensaje de colisión
        if self.collision_message and pygame.time.get_ticks() < self.message_timer:
            msg = self.font.render(self.collision_message, True, (255, 255, 0))
            self.surface.blit(msg, (self.width // 2 - msg.get_width() // 2, 500))

        # Mensaje temporal de status
        if self.status_message and pygame.time.get_ticks() < self.status_timer:
            status = self.font.render(self.status_message, True, self.status_color)
            self.surface.blit(status, (self.width // 2 - status.get_width() // 2, 460))

        # Dibujar hits - CORREGIDA LA INDENTACIÓN
        if hasattr(self, 'hits') and self.hits:
            for hit in self.hits:
                row, col = hit
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                # Dibujar un rectángulo rojo más grande y visible
                pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(x+2, y+2, self.cellSz-4, self.cellSz-4))
                # Dibujar una X blanca encima para mayor contraste
                pygame.draw.line(self.surface, (255, 255, 255), (x + 5, y + 5), 
                                (x + self.cellSz - 5, y + self.cellSz - 5), 2)
                pygame.draw.line(self.surface, (255, 255, 255), (x + self.cellSz - 5, y + 5), 
                                (x + 5, y + self.cellSz - 5), 2)
                #logger.debug(f"[DRAW] Dibujando hit en ({row},{col}) en posición ({x},{y})")
        
        # Dibujar misses
        if hasattr(self, 'misses') and self.misses:
            for miss in self.misses:
                row, col = miss
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                # Dibujar un círculo azul más visible
                pygame.draw.circle(self.surface, (0, 0, 255), 
                                (x + self.cellSz // 2, y + self.cellSz // 2), 
                                self.cellSz // 3, 0)  # Relleno
                # Borde blanco para mayor contraste
                pygame.draw.circle(self.surface, (255, 255, 255), 
                                (x + self.cellSz // 2, y + self.cellSz // 2), 
                                self.cellSz // 3, 2)  # Borde
                #logger.debug(f"[DRAW] Dibujando miss en ({row},{col}) en posición ({x},{y})")
        
        # Depuración de hits y misses - AÑADIDO PARA VERIFICAR
        if hasattr(self, 'hits') and hasattr(self, 'misses') and (self.hits or self.misses):
            debug_text = f"Hits: {self.hits}, Misses: {self.misses}"
            debug_surf = self.font.render(debug_text, True, (255, 255, 0))
            self.surface.blit(debug_surf, (10, 10))
    def draw_confirmation_dialog(self):
       # Fondo del cuadro
        pygame.draw.rect(self.surface, (0, 0, 0), (200, 200, 400, 200))
        pygame.draw.rect(self.surface, (255, 255, 255), (200, 200, 400, 200), 2)

        # Texto
        text = self.font.render("¿Estás seguro de tus posiciones?", True, (255, 255, 255))
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 230))

        # Botones
        pygame.draw.rect(self.surface, (0, 200, 0), self.btnConfirmYes)
        pygame.draw.rect(self.surface, (200, 0, 0), self.btnConfirmNo)

        yes_text = self.font.render("Sí", True, (255, 255, 255))
        no_text = self.font.render("No", True, (255, 255, 255))

        self.surface.blit(yes_text, self.btnConfirmYes.move(25, 10))
        self.surface.blit(no_text, self.btnConfirmNo.move(25, 10))

    def draw_setup(self):
        # Draw grid
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

        has_collisions = self.has_ship_collisions()

        # Draw ships
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)

        # Draw buttons
        button_color = (100, 100, 100) if has_collisions else (0, 200, 0) # Cambiado a verde si no hay colisiones
        pygame.draw.rect(self.surface, button_color, self.btnContinue)

        textContinue = self.font.render('Continue', True, (255, 255, 255))
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        self.surface.blit(textContinue, rectContinue)

        # Instructions
        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

        if has_collisions:
            warning = self.font.render('The ships are overlapped! Reposition them.', True, (255, 255, 0))
            self.surface.blit(warning, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 40))

        if self.show_confirmation:
            self.draw_confirmation_dialog()

        if hasattr(self, 'status_message') and pygame.time.get_ticks() < self.status_timer:
            status = self.font.render(self.status_message, True, self.status_color)
            self.surface.blit(status, (self.width // 2 - status.get_width() // 2, 550))

        # Botón End Turn
        if self.state == "playing":
            color_btn = (100, 200, 100) if self.shot_made else (100, 100, 100)
            pygame.draw.rect(self.surface, color_btn, self.btnEndTurn)
            btn_text = self.font.render("End Turn", True, (0, 0, 0))
            self.surface.blit(btn_text, btn_text.get_rect(center=self.btnEndTurn.center))

    def draw_playing(self):
        logger = logging.getLogger(__name__)
        
        # Dibujar tablero del jugador (izquierda)
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                if self.player and self.player.board.grid[row][col] == 's':
                    pygame.draw.rect(self.surface, (255, 255, 255), rect)  # barcos propios
                elif self.player and self.player.board.grid[row][col] == 'x':
                    pygame.draw.line(self.surface, (255, 0, 0), (x, y), (x + self.cellSz, y + self.cellSz), 2)
                    pygame.draw.line(self.surface, (255, 0, 0), (x + self.cellSz, y), (x, y + self.cellSz), 2)
                elif self.player and self.player.board.grid[row][col] == 'o':
                    pygame.draw.circle(self.surface, (0, 0, 255), (x + self.cellSz//2, y + self.cellSz//2), self.cellSz//3)

        # Dibujar tablero del oponente (derecha)
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

        # Dibujar botón de end turn si es tu turno y ya disparaste
        if self.shot_made and not self.game_over:
            pygame.draw.rect(self.surface, (0, 128, 0), self.btnEndTurn)
            text = self.font.render("End Turn", True, (255, 255, 255))
            self.surface.blit(text, text.get_rect(center=self.btnEndTurn.center))
            #logger.debug("[DRAW] Mostrando botón 'End Turn' porque el disparo ya fue hecho.")


    def draw_game_over(self):
        self.state = "game_over"
        self.title = "GAME OVER"

        textReset = self.font.render('RESET GAME', True, (255, 255, 255))
        rectReset = textReset.get_rect(center=self.btnReset.center)
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset)
        self.surface.blit(textReset, rectReset)

        game_over_text = self.font.render(f"{self.winner} WINS!", True, (255, 255, 0))
        message_win = game_over_text.get_rect(center=(self.width // 2, 300))
        self.surface.blit(game_over_text, message_win)

    def handle_events(self, events):
        if self.state == "setup":
            for event in events:
                for ship in self.ships:
                    ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz, self.ships)

        elif self.state == "playing":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    action = self.handle_click(mouse_pos)
                    logger.debug(f"[EVENTS] Click en {mouse_pos}, acción: {action}")
                    if action == "shot_made":
                        logger.debug("[EVENTS] Disparo realizado")
                        # No hacer nada más, esperar resultado
                    elif action == "end_turn" and self.shot_made:
                        logger.debug("[EVENTS] Finalizando turno")
                        self.end_turn()


    def handle_click(self, mouse_pos):
        logger = logging.getLogger(__name__)
        
        if self.show_confirmation:
            if self.btnConfirmYes.collidepoint(mouse_pos):
                self.show_confirmation = False
                return "continue"
            elif self.btnConfirmNo.collidepoint(mouse_pos):
                self.show_confirmation = False
                return None

        elif self.state == "setup":
            if self.btnContinue.collidepoint(mouse_pos):
                if not self.has_ship_collisions():
                    self.show_confirmation = True

        elif self.state == "playing":
            logger.debug(f"[DEBUG] Estado actual en clic: {self.state}, shot_made: {self.shot_made}")

            # Check if the click is on the attack grid
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        logger.debug(f"[DEBUG] Click detectado en ataque: fila {row}, col {col}")
                        # Solo procesar el ataque si estamos en estado playing y no hemos disparado aún
                        if not self.shot_made:
                            return self.handle_attack(mouse_pos, row, col)
                        else:
                            logger.debug("[DEBUG] Ya se realizó un disparo este turno")
                            return None

            # Check if click was on End Turn button
            if self.btnEndTurn.collidepoint(mouse_pos) and self.shot_made:
                logger.debug("[DEBUG] Clic en End Turn válido.")
                return "end_turn"

        return None

    def handle_attack(self, mouse_pos, row, col):
        logger = logging.getLogger(__name__)
        logger.debug(f"[ATTACK] Intentando atacar ({row},{col})")

        if not self.connection or not self.connection.connected:
            logger.error("[ATTACK] Conexión cerrada.")
            return None

        if self.shot_made:
            logger.warning("[ATTACK] Ya disparaste este turno.")
            return None

        if self.game_over:
            logger.warning("[ATTACK] El juego terminó.")
            return None

        if (row, col) in self.hits or (row, col) in self.misses:
            logger.info(f"[ATTACK] Ya disparaste a ({row},{col}) antes.")
            return None

        try:
            # Enviar el ataque
            self.connection.enviar_datos({"type": "attack", "row": row, "col": col})
            logger.debug("[ATTACK] Ataque enviado correctamente.")
            
            # Marcar que ya se realizó un disparo este turno
            self.shot_made = True
            
            # Actualizar la interfaz para mostrar que se está esperando respuesta
            self.status_message = "Esperando resultado..."
            self.status_timer = pygame.time.get_ticks() + 5000
            self.status_color = (255, 255, 0)
            
            # Forzar actualización de la pantalla
            self.force_update()
            
            self.debug_state()
            return "shot_made"
        except Exception as e:
            logger.exception("[ATTACK] Excepción durante el ataque.")
            return None
            
    def wait_for_opponent_turn(self):

        logger = logging.getLogger(__name__)

        if not self.connection or not hasattr(self.connection, "canal"):
            logger.error("[WAIT] No hay conexión activa o canal no disponible.")
            self.status_message = "Conexión no disponible."
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            self._cerrar_por_desconexion("Canal inválido en conexión.")
            return

        try:
            ready, _, _ = select.select([self.connection.canal], [], [], 0.1)
            if ready:
                datos = self.connection.canal.recv(self.connection.bufsize).decode("utf-8")
                if not datos:
                    logger.error("[WAIT] El socket fue cerrado por el otro extremo.")
                    self._cerrar_por_desconexion("El socket se cerró inesperadamente.")
                    return

                self._recv_buffer += datos
                while '\n' in self._recv_buffer:
                    raw, self._recv_buffer = self._recv_buffer.split('\n', 1)
                    try:
                        msg = json.loads(raw)
                        self._procesar_mensaje_red(msg)
                    except json.JSONDecodeError as e:
                        logger.warning(f"[WAIT] JSON inválido recibido: {e}")

        except Exception as e:
            logger.error(f"[WAIT] Error en select/recv: {e}")
            self.status_message = "Error de red"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            self._cerrar_por_desconexion(f"Error de red: {e}")
        
        if self.hits or self.misses:
            self.draw()
            pygame.display.update()

    def _procesar_mensaje_red(self, msg):
        logger = logging.getLogger(__name__)
        logger.debug(f"[RED] Mensaje recibido: {msg}")

        if not isinstance(msg, dict) or "type" not in msg:
            logger.warning("[RED] Mensaje no válido recibido: %s", msg)
            return

        if msg["type"] == "ping":
            self.connection.enviar_datos({"type": "pong"})

        elif msg["type"] == "turn_ready":
            logger.debug("[RED] Turno recibido, es tu turno ahora.")
            self.switch_to_playing()

        elif msg["type"] == "turn_complete":
            logger.debug("[RED] Turno del oponente finalizado. Es tu turno ahora.")
            self.switch_to_playing()

        elif msg["type"] == "attack":
            if not all(k in msg for k in ("row", "col")):
                logger.warning("[RED] Paquete 'attack' incompleto.")
                return

            row, col = msg["row"], msg["col"]
            logger.debug(f"[RED] Ataque recibido en ({row},{col})")

            if not self.player or not self.opponent:
                logger.error("[RED] Estado inválido, player u opponent son None.")
                self._cerrar_por_desconexion("Estado inválido.")
                return

            try:
                # Usar correctamente el método shoot_at_opponent
                # El jugador actual (self.player) dispara al oponente (self.opponent)
                result = self.opponent.shoot_at_opponent(self.player, row, col)
                logger.debug(f"[RED] Resultado del disparo: {result}")

                self.connection.enviar_datos({
                    "type": "result",
                    "result": result,
                    "row": row,
                    "col": col
                })

                victoria = self.opponent.all_ships_sunken()
                if victoria:
                    self.game_over = True
                    self.winner = f"Player {self.player_number}"
                    self.connection.enviar_datos({
                        "type": "victory",
                        "winner": self.player_number
                    })
                else:
                    self.shot_made = False
                    self.state = "waiting_for_opponent"

            except Exception as e:
                logger.exception("[RED] Error al procesar ataque")

        elif msg["type"] == "result":
            logger.debug(f"[RESULT] Resultado recibido: {msg}")
            row, col = msg.get("row"), msg.get("col")
            result = msg.get("result")

            if row is None or col is None:
                logger.warning("[RESULT] Falta coordenada en el mensaje result.")
                return

            if result == "Disparo exitoso":
                self.hits.append((row, col))
                self.last_result_message = "X ¡Le diste!"
            else:
                self.misses.append((row, col))
                self.last_result_message = "O Fallaste"

            self.last_result_time = pygame.time.get_ticks()
            self.shot_made = True
            logger.debug(f"[RESULT] Se actualizó hits/misses: {self.hits=} {self.misses=}")
            self.draw()  # para asegurar que se muestre el impacto

        elif msg["type"] == "victory":
            self.game_over = True
            self.winner = f"Player {msg['winner']}"
            self.state = "game_over"
            logger.info(f"[VICTORY] El ganador es Player {msg['winner']}")

                
    def end_turn(self):
        logger = logging.getLogger(__name__)

        if not self.connection or not self.connection.connected:
            logger.warning("[END TURN] No hay conexión activa.")
            return

        if not self.shot_made:
            logger.warning("[END TURN] Intento de finalizar turno sin disparar.")
            self.status_message = "¡Debes hacer un disparo primero!"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            return

        try:
            logger.debug("[END TURN] Enviando 'turn_complete' al oponente...")
            self.connection.enviar_datos({"type": "turn_complete"})

            # Cambiar estado local
            self.state = "waiting_for_opponent"
            self.shot_made = False

            # Mensaje en pantalla
            self.status_message = "Esperando turno del oponente..."
            self.status_color = (255, 255, 0)
            self.status_timer = pygame.time.get_ticks() + 5000

            logger.debug("[END TURN] Turno finalizado, esperando oponente.")

        except Exception as e:
            logger.exception("[END TURN] Error al finalizar turno.")
            self.status_message = "Error de red al finalizar turno."
            self.status_color = (255, 0, 0)
            self.status_timer = pygame.time.get_ticks() + 5000
        
    def _cerrar_por_desconexion(self, motivo="Desconexión"):
        self.state = "disconnected"
        self.game_over = True
        self.winner = motivo
        self.status_message = motivo
        self.status_timer = pygame.time.get_ticks() + 5000


    def reset_shot_flag(self):
        self.shot_made = False

    def debug_state(self):
        """Imprime el estado actual del juego para depuración"""
        logger = logging.getLogger(__name__)
        logger.debug("=== ESTADO DEL JUEGO ===")
        logger.debug(f"Estado: {self.state}")
        logger.debug(f"Shot made: {self.shot_made}")
        logger.debug(f"Hits: {self.hits}")
        logger.debug(f"Misses: {self.misses}")
        logger.debug(f"Último resultado: {self.last_result_message}")
        logger.debug("=====================")

    def force_update(self):
        """Fuerza una actualización completa de la pantalla"""
        self.draw()
        pygame.display.update()
        logger.debug("[UPDATE] Forzando actualización de pantalla")

    def procesar_resultado(self, row, col, resultado):
        """Procesa directamente un resultado de ataque y actualiza la interfaz"""
        logger = logging.getLogger(__name__)
        
        # Convertir a enteros si es necesario
        try:
            row = int(row)
            col = int(col)
        except (TypeError, ValueError):
            logger.error(f"[RESULT] Valores inválidos para row/col: {row}/{col}")
            return
        
        # Inicializar arrays si no existen
        if not hasattr(self, 'hits') or self.hits is None:
            self.hits = []
        if not hasattr(self, 'misses') or self.misses is None:
            self.misses = []
        
        # Actualizar arrays y mensajes
        if resultado == "Disparo exitoso":
            if (row, col) not in self.hits:
                self.hits.append((row, col))
                logger.debug(f"[RESULT] Añadido hit en ({row},{col}). Hits actuales: {self.hits}")
        else:
            if (row, col) not in self.misses:
                self.misses.append((row, col))
                logger.debug(f"[RESULT] Añadido miss en ({row},{col}). Misses actuales: {self.misses}")
        
        # Actualizar mensajes
        self.last_result_message = "X ¡Le diste!" if resultado == "Disparo exitoso" else "O Fallaste"
        self.last_result_time = pygame.time.get_ticks()
        self.status_message = self.last_result_message
        self.status_color = (0, 255, 0) if "¡Le diste!" in self.last_result_message else (255, 255, 0)
        self.status_timer = pygame.time.get_ticks() + 3000
        
        # Forzar redibujado
        self.draw()
        pygame.display.update()
        logger.debug(f"[RESULT] Resultado procesado y dibujado: {self.last_result_message} en ({row},{col})")
        self.debug_state()