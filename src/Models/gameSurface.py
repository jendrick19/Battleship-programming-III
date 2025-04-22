import pygame
from src.Models.board import Board
from src.Game.player import Player
from src.Game.gameLogic import GameLogic
from src.Models.ship import Ship

class GameSurface:
    def __init__(self, title, width, height, colorT):
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
        self.backSur= pygame.image.load("6292.jpg")
        self.backSur = pygame.transform.scale(self.backSur, (self.width, self.height))
        self.font_tittle= pygame.font.Font(None, 36)
        self.show_confirmation = False
        self.option_allow_reshoot = True
    
        # Para fase "jugando"
        self.offset_x1, self.offset_y1 = 50, 100  # Position grid
        self.offset_x2, self.offset_y2 = 450, 100  # Attack grid

        self.font = pygame.font.Font(None, 24)
        self.coord_font = pygame.font.Font(None, 20)  # Smaller font for coordinates

        # seguimiento de fases
        self.state = "setup"  # "setup" o "playing"
        self.player_number = 0
        if "player 1" in title.lower():
            self.player_number = 1
        elif "player 2" in title.lower():
            self.player_number = 2

        # botones
        self.btnContinue = pygame.Rect((self.width - 90) // 2, 500, 90, 50)
        self.btnReset = pygame.Rect(340, 400, 120, 50)
        self.btnEndTurn = pygame.Rect((self.width - 90) // 2, 500, 90, 50)
        self.btnConfirmYes = pygame.Rect(300 ,300, 80, 40)
        self.btnConfirmNo = pygame.Rect(410, 300, 80, 40)
        
        # Botones para mover barcos
        self.btnMoveUp = pygame.Rect(60, 450, 40, 40)
        self.btnMoveDown = pygame.Rect(60, 550, 40, 40)
        self.btnMoveLeft = pygame.Rect(20, 500, 40, 40)
        self.btnMoveRight = pygame.Rect(100, 500, 40, 40)
        
        # Boton para disparar
        self.btncoords = pygame.Rect(580, 450, 160, 40)
        self.active = False
        
        self.input_text = ""
        self.colorI = (0,0,0)
        self.colorA = (0, 255, 0)
        
        self.error_message = "" 

        # Estado para selección de barco
        self.selected_ship = None
        self.ship_selection_active = False
        
        # Control de acciones por turno
        self.action_taken = False  # Indica si ya se realizó una acción (mover o disparar)
        
        # Rastreo de posiciones dañadas en el tablero
        self.damaged_positions = set()  # Conjunto de posiciones (row, col) donde se ha dañado un barco

        # Barcos para la fase de configuración
        self.ships = []
        if self.state == "setup":
            self.ships = [
                Ship(4, 0, 0, True),
                Ship(3, 0, 2, True),
                Ship(2, 0, 4, True),
                Ship(2, 0, 6, True),
                Ship(1, 0, 8, True)
            ]

        # Objetos de juego
        self.player = None
        self.opponent = None
        self.game_logic = None

        # seguimiento de usuario y oponente
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

        # dibujar el título
        title = self.font_tittle.render(self.title, True, self.colorT )
        title_rect = title.get_rect(center=(self.width // 2, 25))
        self.surface.blit(title, title_rect)

        if self.game_over:
            self.draw_game_over()
        elif self.state == "setup":
            self.draw_setup()
        else:
            self.draw_playing()

        if self.collision_message and pygame.time.get_ticks() < self.message_timer:
            message = self.font.render(self.collision_message, True, (255, 255, 0))
            self.surface.blit(message, (self.width // 2 - message.get_width() // 2, 475))

    def draw_coordinates(self, offset_x, offset_y):
        # Dibujar nombres de filas (A-J)
        for row in range(self.gridSz):
            row_label = self.coord_font.render(chr(65 + row), True, (255, 255, 255))
            self.surface.blit(row_label, (offset_x - 20, offset_y + row * self.cellSz + self.cellSz // 2 - 5))
        
        # Dibujar nombres de columnas (1-10)
        for col in range(self.gridSz):
            col_label = self.coord_font.render(str(col + 1), True, (255, 255, 255))
            self.surface.blit(col_label, (offset_x + col * self.cellSz + self.cellSz // 2 - 5, offset_y - 20))

    def draw_coordinates_button(self):
        # dibujar formato de las coordenadas
        format_text = self.font.render("Format: A1 or B5", True, (255, 255, 255))
        self.surface.blit(format_text, (self.btncoords.x + 5, self.btncoords.y - 20))

        self.color = self.colorA if self.active else self.colorI # Cambiado a verde si el botón está activo
       
        # Dibuja el botón de las coordenadas
        pygame.draw.rect(self.surface, self.color, self.btncoords, 2)
        button_text = self.input_text if self.active else "Enter coordinates"
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.btncoords.center)
        self.surface.blit(text_surface, text_rect)
        
        #Dibujar nombre de los barcos y obtener posicion de barcos
    def draw_name_ships(self):
        ship_names = ["Aircraft Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        name_positions_y = []
        y_offset = -10
        for name in ship_names:
            text_surface = self.font.render(name, True, (255, 255, 255))
            if not self.selected_ship:
                self.surface.blit(text_surface, (self.btncoords.x - 530, self.btncoords.y + y_offset))
                
            name_positions_y.append(self.btncoords.y + y_offset + self.font.get_linesize() // 2) # Guardar la posición y central vertical
            y_offset += 20
        return name_positions_y
            
    def handle_attack_input(self, input_text):
        self.error_message = ""
        # Validar input (e.g., "A1", "B5")
        if len(input_text) < 2 or not input_text[0].isalpha() or not input_text[1:].isdigit():
            self.error_message = "Invalid coordinate format!"
            self.active = False
            return self.error_message

        # Convertir input a coordenadas de la cuadricula
        row = ord(input_text[0].upper()) - ord('A')  # Convertir letra a número (A=0, B=1, ...)
        col = int(input_text[1:]) - 1  # Convertir número a índice (1=0, 2=1, ...)

        # Revisar si las coordenadas están dentro de los límites de la cuadrícula
        if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
            self.handle_attack(None, row, col)  # Llamar a la función de ataque con las coordenadas
            self.action_taken = True
            self.active = False
        else:
            self.error_message = "Coordinates out of bounds!"
            self.active = False
            return self.error_message   

    def draw_confirmation_dialog(self):
       # Fondo del cuadro de confirmación
        pygame.draw.rect(self.surface, (0, 0, 0), (200, 200, 400, 200))
        pygame.draw.rect(self.surface, (255, 255, 255), (200, 200, 400, 200), 2)

        # Texto
        text = self.font.render("Are you sure of your positions?", True, (255, 255, 255))
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 230))

        # Botones
        pygame.draw.rect(self.surface, (0, 200, 0), self.btnConfirmYes)
        pygame.draw.rect(self.surface, (200, 0, 0), self.btnConfirmNo)

        yes_text = self.font.render("Yes", True, (255, 255, 255))
        no_text = self.font.render("No", True, (255, 255, 255))

        self.surface.blit(yes_text, self.btnConfirmYes.move(28, 12))
        self.surface.blit(no_text, self.btnConfirmNo.move(28, 12))

    def draw_setup(self):
        # Dibujar cuadrícula de posiciones
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

        # Dibujar coordinadas para la cuadrícula de posiciones
        self.draw_coordinates(self.offset_x, self.offset_y)

        has_collisions = self.has_ship_collisions()

        # Dibujar barcos
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)

        # Dibujar botones de continuar
        button_color = (100, 100, 100) if has_collisions else (0, 200, 0) # Cambiado a verde si no hay colisiones
        pygame.draw.rect(self.surface, button_color, self.btnContinue)

        textContinue = self.font.render('Continue', True, (255, 255, 255))
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        self.surface.blit(textContinue, rectContinue)

        # Instrucciones de rotación
        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

        if has_collisions:
            warning = self.font.render('The ships are overlapped! Reposition them.', True, (255, 255, 0))
            self.surface.blit(warning, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 40))

        if self.show_confirmation:
            self.draw_confirmation_dialog()

    def draw_playing(self):
        # Dibujar cuadrícula de posiciones
        titlePosit = self.font.render('POSITIONS', True, (255, 255, 255))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 50))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                # Dibujar posiciones dañadas (donde había un barco pero se movió)
                if (row, col) in self.damaged_positions and (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.circle(self.surface, (150, 150, 150),
                                      (x + self.cellSz // 2, y + self.cellSz // 2),
                                      self.cellSz // 3,
                                      3)

        # Dibujar coordenadas para la cuadrícula de posiciones
        self.draw_coordinates(self.offset_x1, self.offset_y1)

        # Dibujar barcos
        for ship in self.player.ships:
            is_selected = (ship == self.selected_ship)
            
            # Dibujar cada segmento del barco
            for i, pos in enumerate(ship.position):
                row, col = pos
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                
                # Color según estado: dañado, seleccionado o normal
                if ship.damage_positions[i]:
                    color = (255, 0, 0)
                elif is_selected:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 0)
                    
                pygame.draw.rect(self.surface, color, rect)

        # Dibujar cuadrícula de ataque
        titleAttck = self.font.render('ATTACK', True, (255, 255, 255))
        self.surface.blit(titleAttck, (self.offset_x2 + 120, self.offset_y2 - 50))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                # Dibujar hits (X roja)
                if (row, col) in self.hits:
                    pygame.draw.line(self.surface, (255, 0, 0),
                                     (x + 5, y + 5),
                                     (x + self.cellSz - 5, y + self.cellSz - 5),
                                     3)
                    pygame.draw.line(self.surface, (255, 0, 0),
                                     (x + self.cellSz - 5, y + 5),
                                     (x + 5, y + self.cellSz - 5),
                                     3)

                # Dibujar misses (círculo blanco)
                if (row, col) in self.misses:
                    pygame.draw.circle(self.surface, (255, 255, 255),
                                        (x + self.cellSz // 2, y + self.cellSz // 2),
                                        self.cellSz // 3,
                                        3)

        # Dibujar coordinadas para la cuadrícula de ataque
        self.draw_coordinates(self.offset_x2, self.offset_y2)

        # Dibujar boton de finalizar turno
        button_color = (255, 0, 0) if self.action_taken else (100, 100, 100)
        pygame.draw.rect(self.surface, button_color, self.btnEndTurn)

        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)
        self.surface.blit(textEndTurn, rectEndTurn)

        # Dibujar botón de coordenadas
        self.draw_coordinates_button()
        
        #Dibujar nombre de barcos
        

        # Dibujar botones de movimiento si hay un barco seleccionado y no se ha realizado una acción
        if self.selected_ship and not self.action_taken:
            # Botón arriba
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveUp)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(60 + 20, 450 + 10), (60 + 10, 450 + 30), (60 + 30, 450 + 30)])
            
            # Botón abajo
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveDown)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(60 + 20, 550 + 30), (60 + 10, 550 + 10), (60 + 30, 550 + 10)])
            
            # Botón izquierda
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveLeft)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(20 + 10, 500 + 20), (20 + 30, 500 + 10), (20 + 30, 500 + 30)])
            
            # Botón derecha
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveRight)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(100 + 30, 500 + 20), (100 + 10, 500 + 10), (100 + 10, 500 + 30)])
            
            # Instrucciones para mover barcos
            move_text = self.font.render("Move your ship", True, (255, 255, 255))
            self.surface.blit(move_text, (20, 430))

        ship_name_positions_y = self.draw_name_ships()
        # Display game status
        if self.player and self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (670, 545))
            
            for i, ship in enumerate(self.opponent.ships):
                if ship.check_sunken_ship():
                    y_position = ship_name_positions_y[i]
                    
                    if not self.selected_ship:
                        pygame.draw.line(self.surface, (100, 100, 100),
                                     (self.btncoords.x - 530 - 20, y_position), # Ajustar inicio de la línea
                                     (self.btncoords.x - 530 + 150, y_position), # Ajustar fin de la línea
                                     3)
            
            # Display turn status
            if self.action_taken:
                if self.shot_made:
                    turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
                else:
                    turn_status = self.font.render("Ship moved! Click End Turn", True, (255, 255, 0))
                self.surface.blit(turn_status, (300, 450))

            elif not self.action_taken and self.error_message == "Invalid coordinate format!":
                turn_status = self.font.render("Invalid coordinate format!", True, (255, 0, 0))
                self.surface.blit(turn_status, (300, 450))

            elif not self.action_taken and self.error_message == "Coordinates out of bounds!":
                turn_status = self.font.render("Coordinates out of bounds!", True, (255, 0, 0))
                self.surface.blit(turn_status, (300, 450))

            else:
                turn_status = self.font.render("Move a ship or Make a shot", True, (255, 255, 255))
                self.surface.blit(turn_status, (300, 450))

    def draw_game_over(self):
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
        if self.state == "playing":
            for event in events:   
                mouse_pos = pygame.mouse.get_pos()    
                if not self.action_taken:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btncoords.collidepoint(mouse_pos):
                            self.active = True
                        else:
                            self.active = False
                    if event.type == pygame.KEYDOWN and self.active:
                        if event.key == pygame.K_RETURN:
                            self.handle_attack_input(self.input_text)
                            self.input_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode
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


            # Si ya se realizó una acción, solo permitir finalizar el turno
            if self.action_taken:
                if self.btnEndTurn.collidepoint(mouse_pos):
                    return "end_turn"
                return None
                
            # Verificar si se hizo clic en los botones de movimiento
            if self.selected_ship:
                if self.btnMoveUp.collidepoint(mouse_pos):
                    return self.move_selected_ship('up')
                elif self.btnMoveDown.collidepoint(mouse_pos):
                    return self.move_selected_ship('down')
                elif self.btnMoveLeft.collidepoint(mouse_pos):
                    return self.move_selected_ship('left')
                elif self.btnMoveRight.collidepoint(mouse_pos):
                    return self.move_selected_ship('right')
            
            # Verificar si se hizo clic en el tablero de posiciones para seleccionar un barco
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x1 + col * self.cellSz
                    y = self.offset_y1 + row * self.cellSz
                    position_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    
                    if position_rect.collidepoint(mouse_pos):
                        return self.handle_ship_selection(row, col)
            
            # Verificar si se hizo clic en el tablero de ataque
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        # Deseleccionar barco al atacar
                        self.selected_ship = None
                        return self.handle_attack(mouse_pos, row, col)

            # revisar si se hizo clic en el botón de finalizar turno
            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.action_taken or self.game_over:
                    # Deseleccionar barco al finalizar turno
                    self.selected_ship = None
                    return "end_turn"
        return None
    
    
    def handle_ship_selection(self, row, col):
        # Verificar si hay un barco en la posición seleccionada
        for ship in self.player.ships:
            if (row, col) in ship.position:
                # Si ya estaba seleccionado, deseleccionarlo
                if self.selected_ship == ship:
                    self.selected_ship = None
                else:
                    self.selected_ship = ship
                return "ship_selected"
        
        # Si no hay barco, deseleccionar
        self.selected_ship = None
        return None
    
    def move_selected_ship(self, direction):
        if not self.selected_ship or self.action_taken:
            return None

        # Verificar si el barco puede moverse según las reglas de daño
        if not self.can_ship_move(self.selected_ship):
            self.collision_message = "Engine damage. You can't move"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None
    
        # Guardar las posiciones actuales del barco antes de moverlo
        old_positions = self.selected_ship.position.copy()
        
        # Verificar si el barco puede moverse en esa dirección
        if self.selected_ship.can_move(direction, self.gridSz, self.player.ships):
            # Registrar las posiciones dañadas antes de mover
            for idx, pos in enumerate(old_positions):
                if self.selected_ship.damage_positions[idx]:
                    self.damaged_positions.add(pos)
            
            # Mover el barco
            self.selected_ship.move(direction)
    
            # Actualizar el tablero del jugador
            self.update_player_board()
            
            # Marcar que se ha realizado una acción
            self.action_taken = True
            
            return "ship_moved"
        else:
            # Mostrar mensaje de que no se puede mover
            self.collision_message = "The ship cannot be moved in this direction"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None
    
    def clear_shots_at_ship_positions(self, ship):
        """Elimina las posiciones del barco del historial de disparos"""
        for pos in ship.position:
            # Eliminar de hits si existe
            if pos in self.opponent.hits:
                self.opponent.hits.remove(pos)
                if pos in self.hits:
                    self.hits.remove(pos)
            
            # Eliminar de misses si existe
            if pos in self.opponent.misses:
                self.opponent.misses.remove(pos)
                if pos in self.misses:
                    self.misses.remove(pos)
    
    def can_ship_move(self, ship):
        if ship.life == ship.length:
            return True
            
        # Para barcos de longitud 1, no pueden moverse si están dañados
        if ship.length == 1:
            return False
            
        # Para barcos más largos, verificar si el daño está en posiciones internas
        for idx in range(1, ship.length - 1):  # Posiciones internas (1 a length-2)
            if ship.damage_positions[idx]:
                return False  # No puede moverse si hay daño en posiciones internas
            
        # Si solo hay daño en los extremos, puede moverse
        return True
            
    
    def update_player_board(self):
        # Limpiar el tablero
        self.player.board.grid = [['w' for _ in range(self.player.board.size)] for _ in range(self.player.board.size)]
        
        # Marcar las posiciones de disparos fallidos como 'o'
        if hasattr(self.opponent, 'misses'):
            for row, col in self.opponent.misses:
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Solo marcar como 'o' si no hay un barco en esa posición
                    if (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                        self.player.board.grid[row][col] = 'o'
        
        # Actualizar posiciones de los barcos en el tablero
        for ship in self.player.ships:
            for idx, (row, col) in enumerate(ship.position):
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Marcar como 's' si no está dañada, o como 'x' si está dañada
                    if ship.damage_positions[idx]:
                        self.player.board.grid[row][col] = 'x'  # Parte dañada del barco
                    else:
                        self.player.board.grid[row][col] = 's'  # Parte intacta del barco

    def handle_attack(self, mouse_pos, row, col):
        # no permitir disparar si ya se realizó una acción o si el juego ha terminado
        if self.action_taken or not self.player or not self.opponent or self.game_over:
            return None

        if self.option_allow_reshoot:
        # Verificar si hay un barco en la posición
            has_ship = False
            ship_already_damaged = False
            target_ship = None
            position_index = -1
        
            for ship in self.opponent.ships:
                if (row, col) in ship.position:
                    has_ship = True
                    target_ship = ship
                    position_index = ship.position.index((row, col))
                    # Verificar si esa parte del barco ya está dañada
                    if position_index >= 0 and ship.damage_positions[position_index]:
                        ship_already_damaged = True
                    break
        
        # Si hay un barco, la posición está en misses, y esa parte del barco NO está dañada, permitir re-atacar
            if has_ship and (row, col) in self.misses and not ship_already_damaged:
                # Remover de la lista de misses ya que ahora será un hit
                self.misses.remove((row, col))
        # Si no hay barco, ya es un hit, o esa parte del barco ya está dañada, no permitir re-atacar
            elif (row, col) in self.hits or (row, col) in self.misses:
                return None

        # usar clase jugador para disparar a el oponente
        result = self.player.shoot_at_opponent(self.opponent, row, col)

        if result == "Disparo exitoso":
            self.hits.append((row, col))
            
            # Registrar la posición dañada en el oponente
            for ship in self.opponent.ships:
                if (row, col) in ship.position:
                    # Añadir a las posiciones dañadas del oponente
                    if hasattr(self.opponent, 'damaged_positions'):
                        self.opponent.damaged_positions.add((row, col))
                    break
        else:
            self.misses.append((row, col))

        # revisar si se ha ganado
        victory_message = self.game_logic.check_victory()
        if victory_message:
            self.game_over = True
            self.winner = f"Player {self.player_number}"

        # actualizar variable de accion realizada
        self.action_taken = True
        self.shot_made = True
        return "shot_made"

    def reset_shot_flag(self):
        self.shot_made = False
        self.action_taken = False
        self.selected_ship = None