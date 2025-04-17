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
        self.btnConfirmYes = pygame.Rect(300 ,300, 80, 40)
        self.btnConfirmNo = pygame.Rect(410, 300, 80, 40)
        
        # Botones para mover barcos
        self.btnMoveUp = pygame.Rect(100, 450, 40, 40)
        self.btnMoveDown = pygame.Rect(100, 550, 40, 40)
        self.btnMoveLeft = pygame.Rect(60, 500, 40, 40)
        self.btnMoveRight = pygame.Rect(140, 500, 40, 40)
        
        # Estado para selección de barco
        self.selected_ship = None
        self.ship_selection_active = False
        
        # Control de acciones por turno
        self.action_taken = False  # Indica si ya se realizó una acción (mover o disparar)
        
        # Rastreo de posiciones dañadas en el tablero
        self.damaged_positions = set()  # Conjunto de posiciones (row, col) donde se ha dañado un barco

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

        self.surface.blit(yes_text, self.btnConfirmYes.move(30, 12))
        self.surface.blit(no_text, self.btnConfirmNo.move(30, 12))

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
        # Draw position grid
        titlePosit = self.font.render('POSITIONS', True, (255, 255, 255))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 30))

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
                    color = (255, 0, 0)  # Rojo para partes dañadas
                elif is_selected:
                    color = (0, 255, 0)  # Verde para barco seleccionado
                else:
                    color = (0, 0, 0)    # Negro para barcos normales
                    
                pygame.draw.rect(self.surface, color, rect)

        # Draw attack grid
        titleAttck = self.font.render('ATTACK', True, (255, 255, 255))
        self.surface.blit(titleAttck, (self.offset_x2 + 120, self.offset_y2 - 30))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                # Draw hits (red X)
                if (row, col) in self.hits:
                    pygame.draw.line(self.surface, (255, 0, 0),
                                     (x + 5, y + 5),
                                     (x + self.cellSz - 5, y + self.cellSz - 5),
                                     3)
                    pygame.draw.line(self.surface, (255, 0, 0),
                                     (x + self.cellSz - 5, y + 5),
                                     (x + 5, y + self.cellSz - 5),
                                     3)

                # Draw misses (white circle)
                if (row, col) in self.misses:
                    pygame.draw.circle(self.surface, (255, 255, 255),
                                        (x + self.cellSz // 2, y + self.cellSz // 2),
                                        self.cellSz // 3,
                                        3)

        # Draw end turn button
        button_color = (255, 0, 0) if self.action_taken else (100, 100, 100)
        pygame.draw.rect(self.surface, button_color, self.btnEndTurn)

        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)
        self.surface.blit(textEndTurn, rectEndTurn)

        # Dibujar botones de movimiento si hay un barco seleccionado y no se ha realizado una acción
        if self.selected_ship and not self.action_taken:
            # Botón arriba
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveUp)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(100 + 20, 450 + 10), (100 + 10, 450 + 30), (100 + 30, 450 + 30)])
            
            # Botón abajo
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveDown)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(100 + 20, 550 + 30), (100 + 10, 550 + 10), (100 + 30, 550 + 10)])
            
            # Botón izquierda
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveLeft)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(60 + 10, 500 + 20), (60 + 30, 500 + 10), (60 + 30, 500 + 30)])
            
            # Botón derecha
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveRight)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                               [(140 + 30, 500 + 20), (140 + 10, 500 + 10), (140 + 10, 500 + 30)])
            
            # Instrucciones para mover barcos
            move_text = self.font.render("Move your selected ship", True, (255, 255, 255))
            self.surface.blit(move_text, (10, 430))

        # Display game status
        if self.player and self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (600, 545))

            # Display turn status
            if self.action_taken:
                if self.shot_made:
                    turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
                else:
                    turn_status = self.font.render("Ship moved! Click End Turn", True, (255, 255, 0))
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
            
            # Check if the click is on the attack grid
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        # Deseleccionar barco al atacar
                        self.selected_ship = None
                        return self.handle_attack(mouse_pos, row, col)

            # Check if the click is on the End Turn button
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
            
            # Verificar si alguna parte del barco se ha movido a una posición que ya fue disparada
            # y marcarla como dañada automáticamente
            self.check_for_damage_after_move(self.selected_ship)
            
            # Actualizar el tablero del jugador
            self.update_player_board()
            
            # Marcar que se ha realizado una acción
            self.action_taken = True
            
            return "ship_moved"
        else:
            # Mostrar mensaje de que no se puede mover
            self.collision_message = f"No se puede mover el barco en esa dirección"
            self.message_timer = pygame.time.get_ticks() + 2000  # Mostrar por 2 segundos
            return None
    
    def check_for_damage_after_move(self, ship):
        """Verifica si alguna parte del barco se ha movido a una posición que ya fue disparada"""
        # Obtener todas las posiciones que han sido disparadas (hits y misses del oponente)
        opponent_shots = set()
        if hasattr(self.opponent, 'hits'):
            opponent_shots.update(self.opponent.hits)
        if hasattr(self.opponent, 'misses'):
            opponent_shots.update(self.opponent.misses)
        
        # También incluir las posiciones dañadas registradas
        opponent_shots.update(self.damaged_positions)
        
        # Verificar cada segmento del barco
        for idx, pos in enumerate(ship.position):
            # Si la posición ya fue disparada, marcar esa parte como dañada
            if pos in opponent_shots or pos in self.damaged_positions:
                if not ship.damage_positions[idx]:  # Solo si no estaba ya dañada
                    ship.damage_positions[idx] = True
                    ship.life -= 1  # Reducir la vida del barco
                    # Añadir a las posiciones dañadas
                    self.damaged_positions.add(pos)
    
    def update_player_board(self):
        # Limpiar el tablero, pero mantener las posiciones dañadas como 'o'
        self.player.board.grid = [['w' for _ in range(self.player.board.size)] for _ in range(self.player.board.size)]
        
        # Marcar las posiciones dañadas como 'o' (fallo)
        for row, col in self.damaged_positions:
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
        # Don't allow shooting if a shot has already been made this turn
        if self.action_taken or not self.player or not self.opponent or self.game_over:
            return None

        # Don't allow clicking on already attacked cells
        if (row, col) in self.hits or (row, col) in self.misses:
            return None

        # Use Player class to shoot at opponent
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

        # Check for win condition using GameLogic
        victory_message = self.game_logic.check_victory()
        if victory_message:
            self.game_over = True
            self.winner = f"Player {self.player_number}"

        # Set the action_taken flag to true
        self.action_taken = True
        self.shot_made = True
        return "shot_made"

    def reset_shot_flag(self):
        self.shot_made = False
        self.action_taken = False
        self.selected_ship = None
