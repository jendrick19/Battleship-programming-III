import pygame
import os
from src.Models.board import Board
from src.Game.player import Player
from src.Game.gameLogic import GameLogic
from src.Models.ship import Ship

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

    def has_ship_collisions(self):
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i+1:]:
                if ship1.check_collision([ship2]):
                    return True
        return False

    def draw(self):
        self.surface.fill((3, 37, 108))
        self.surface.blit(self.backSur,(0,0))

        # Draw title
        title = self.font_tittle.render(self.title, True, self.colorT )
        title_rect = title.get_rect(center=(self.width // 2, 45))
        self.surface.blit(title, title_rect)

        if self.game_over:
            self.draw_game_over()
        elif self.state == "setup":
            self.draw_setup()
        else:
            self.draw_playing()

        if self.collision_message and pygame.time.get_ticks() < self.message_timer:
            message = self.font.render(self.collision_message, True, (255, 255, 0))
            self.surface.blit(message, (self.width // 2 - message.get_width() // 2, 500))

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

    def draw_playing(self):
        # Tablero de posiciones (izquierda)
        titlePosit = self.font.render('POSITIONS', True, (255, 255, 255))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 30))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)
                if self.player and (row, col) in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.rect(self.surface, (0, 0, 0), rect)

        # Tablero de ataque (derecha)
        titleAttck = self.font.render('ATTACK', True, (255, 255, 255))
        self.surface.blit(titleAttck, (self.offset_x2 + 120, self.offset_y2 - 30))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                if (row, col) in self.hits:
                    pygame.draw.line(self.surface, (255, 0, 0), (x + 5, y + 5), (x + self.cellSz - 5, y + self.cellSz - 5), 3)
                    pygame.draw.line(self.surface, (255, 0, 0), (x + self.cellSz - 5, y + 5), (x + 5, y + self.cellSz - 5), 3)

                if (row, col) in self.misses:
                    pygame.draw.circle(self.surface, (255, 255, 255), (x + self.cellSz // 2, y + self.cellSz // 2), self.cellSz // 3, 3)

        # Botón End Turn y mensajes según el estado
        if self.state == "waiting_for_opponent":
            pygame.draw.rect(self.surface, (100, 100, 100), self.btnEndTurn)
            textWaiting = self.font.render("Esperando...", True, (200, 200, 200))
            self.surface.blit(textWaiting, self.btnEndTurn.move(15, 10))
            status = self.font.render("Esperando el turno del oponente...", True, (255, 255, 0))
            self.surface.blit(status, (280, 410))
        else:
            pygame.draw.rect(self.surface, (255, 0, 0) if self.shot_made else (100, 100, 100), self.btnEndTurn)
            textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
            self.surface.blit(textEndTurn, self.btnEndTurn.move(10, 10))

            if not self.shot_made:
                turno_msg = self.font.render("Es tu turno", True, (0, 255, 0))
                self.surface.blit(turno_msg, (320, 410))

        # Estado del disparo
        if self.state == "playing":
            if self.shot_made:
                turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
                self.surface.blit(turn_status, (300, 450))
            else:
                turn_status = self.font.render("Make your shot", True, (255, 255, 255))
                self.surface.blit(turn_status, (340, 450))

            if self.last_result_message and pygame.time.get_ticks() - self.last_result_time < 3000:
                color = (255, 0, 0) if "X" in self.last_result_message else (255, 255, 255)
                result_text = self.font.render(self.last_result_message, True, color)
                self.surface.blit(result_text, (self.width // 2 - result_text.get_width() // 2, 480))

        # Barcos hundidos
        if self.player and self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (600, 545))


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

        elif self.state == "playing" and not self.shot_made:
            for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        action = self.handle_click(mouse_pos)
                        if action == "end_turn":
                            self.end_turn()


    def handle_click(self, mouse_pos):
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
            #  Bloqueo si no es tu turno
            if self.shot_made:
                return None

            # Check if the click is on the attack grid
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        return self.handle_attack(mouse_pos, row, col)

            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.shot_made or self.game_over:
                    return "end_turn"

        return None

    def handle_attack(self, mouse_pos, row, col):
        # No permitir disparar si ya se hizo un disparo o el juego terminó
        if self.shot_made or not self.player or not self.opponent or self.game_over:
            return None

        # No permitir disparar a celdas ya atacadas
        if (row, col) in self.hits or (row, col) in self.misses:
            return None

        # Si hay conexión, enviar el ataque por red
        if self.connection:
            self.connection.enviar_datos({
                "type": "attack",
                "row": row,
                "col": col
            })

            response = self.connection.recibir_datos()
            if not response:
                print("No se recibió respuesta del oponente.")
                return None
            result = response.get("result")
        else:
            # En modo local
            result = self.player.shoot_at_opponent(self.opponent, row, col)

        # Guardar mensaje visual
        self.last_result_time = pygame.time.get_ticks()
        if result == "Disparo exitoso":
            self.last_result_message = "X ¡Le diste!"
            self.hits.append((row, col))
        else:
            self.last_result_message = "O Fallaste"
            self.misses.append((row, col))

        # Verificar si se ganó la partida
        victory_message = self.game_logic.check_victory()
        if victory_message:
            self.game_over = True
            self.winner = f"Player {self.player_number}"
            if self.connection:
                self.connection.enviar_datos({
                    "type": "victory",
                    "winner": self.player_number
                })

        # Marcar que se hizo un disparo
        self.shot_made = True
        return "shot_made"
    
    def wait_for_opponent_turn(self):
        if not self.connection:
            print("[WAIT] No hay conexión activa.")
            return

        print("\n[WAIT] ---")
        print("[WAIT] Esperando datos del oponente...")

        data = self.connection.recibir_datos()

        if not data:
            print("[WAIT] No se recibió nada del oponente (timeout o error).")
            return

        print(f"[WAIT] Datos recibidos: {data}")

        if data["type"] == "turn_ready":
            self.state = "playing"
            print("[WAIT] ¡Es tu turno ahora!")
            print("[WAIT] Estado cambiado a: playing")
            print("[WAIT] ---\n")
            return

        if data["type"] == "attack":
            row = data["row"]
            col = data["col"]
            print(f"[WAIT] Recibido ataque en fila {row}, columna {col}")

            # Procesar ataque
            result = self.player.shoot_at_opponent(self.opponent, row, col)
            print(f"[WAIT] Resultado del disparo recibido: {result}")

            # Enviar resultado de vuelta
            self.connection.enviar_datos({
                "type": "result",
                "result": result
            })
            print("[WAIT] Resultado enviado al oponente.")

            # Verificar si terminó el juego
            victory_message = self.game_logic.check_victory()
            if victory_message:
                self.game_over = True
                self.winner = f"Player {3 - self.player_number}"
                print(f"[WAIT] ¡El jugador {self.winner} ha ganado!")
                self.connection.enviar_datos({
                    "type": "victory",
                    "winner": 3 - self.player_number
                })
            else:
                self.state = "waiting_for_opponent"
                self.shot_made = False
                print("[WAIT] Ataque procesado, esperando siguiente acción del oponente.")
                self.draw()

        print("[WAIT] ---\n")

    
    def end_turn(self):
        print("\n[END TURN] ---")
        print(f"[END TURN] Jugador {self.player_number} termina su turno.")
        print(f"[END TURN] Estado actual antes: {self.state}, Disparo hecho: {self.shot_made}")

        self.state = "waiting_for_opponent"
        self.shot_made = False

        if self.connection:
            print("[END TURN] Enviando 'turn_ready' al oponente...")
            self.connection.enviar_datos({
                "type": "turn_ready"
            })
        else:
            print("[END TURN] Sin conexión activa.")

        self.draw()
        print("[END TURN] Estado cambiado a waiting. Redibujado.")
        print("[END TURN] ---\n")

    def reset_shot_flag(self):
        self.shot_made = False