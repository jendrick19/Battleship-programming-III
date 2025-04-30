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
        self.colorT = colorT
        self.gridSz = 10
        self.cellSz = 30
        self.offset_x = 250
        self.offset_y = 100
        self.last_result_message = ""
        self.last_result_time = 0
        ruta_imagen = os.path.join(os.path.dirname(__file__), '..', '..', '6292.jpg')
        self.backSur = pygame.image.load(os.path.abspath(ruta_imagen))
        self.backSur = pygame.transform.scale(self.backSur, (self.width, self.height))
        self.font_tittle = pygame.font.Font(None, 36)
        self.show_confirmation = False
        self.connection = connection  # Conexion por socket
        self._recv_buffer = ""
        self.status_message = ""
        self.status_timer = 0
        self.red_intentos = 0
        self.status_color = (255, 255, 255)  # White as default value
        self.option_allow_reshoot = True

        # For "playing" phase
        self.offset_x1, self.offset_y1 = 50, 100  # Position grid
        self.offset_x2, self.offset_y2 = 450, 100  # Attack grid

        self.font = pygame.font.Font(None, 24)
        self.coord_font = pygame.font.Font(None, 20)  # Smaller font for coordinates

        # Phase tracking
        self.state = "setup"  # "setup" or "playing" or "waiting_for_opponent"
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
        
        # Buttons for moving ships
        self.btnMoveUp = pygame.Rect(60, 450, 40, 40)
        self.btnMoveDown = pygame.Rect(60, 550, 40, 40)
        self.btnMoveLeft = pygame.Rect(20, 500, 40, 40)
        self.btnMoveRight = pygame.Rect(100, 500, 40, 40)
        
        # Button for coordinates
        self.btncoords = pygame.Rect(580, 450, 160, 40)
        self.active = False
        self.input_text = ""
        self.colorI = (0, 0, 0)
        self.colorA = (0, 255, 0)
        self.error_message = ""

        # State for ship selection
        self.selected_ship = None
        self.ship_selection_active = False
        
        # Turn action control
        self.action_taken = False  # Indicates if an action has been taken (move or shoot)
        
        # Tracking damaged positions on the board
        self.damaged_positions = set()  # Set of positions (row, col) where a ship has been damaged

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
        self.action_taken = False

    def has_ship_collisions(self):
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i+1:]:
                if ship1.check_collision([ship2]):
                    return True
        return False

    def draw(self):
        self.surface.fill((3, 37, 108))
        self.surface.blit(self.backSur, (0, 0))

        # Move the title higher
        title = self.font_tittle.render(self.title, True, self.colorT)
        self.surface.blit(title, title.get_rect(center=(self.width // 2, 30)))

        if self.game_over:
            self.draw_game_over()
        elif self.state == "setup":
            self.draw_setup()
        else:
            self.draw_playing()

        # Show collision message
        if self.collision_message and pygame.time.get_ticks() < self.message_timer:
            msg = self.font.render(self.collision_message, True, (255, 255, 0))
            self.surface.blit(msg, (self.width // 2 - msg.get_width() // 2, 500))

        # Temporary status message
        if self.status_message and pygame.time.get_ticks() < self.status_timer:
            status = self.font.render(self.status_message, True, self.status_color)
            self.surface.blit(status, (self.width // 2 - status.get_width() // 2, 460))

        # Draw hits
        if hasattr(self, 'hits') and self.hits:
            for hit in self.hits:
                row, col = hit
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                # Draw a larger and more visible red rectangle
                pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(x+2, y+2, self.cellSz-4, self.cellSz-4))
                # Draw a white X on top for better contrast
                pygame.draw.line(self.surface, (255, 255, 255), (x + 5, y + 5), 
                                (x + self.cellSz - 5, y + self.cellSz - 5), 2)
                pygame.draw.line(self.surface, (255, 255, 255), (x + self.cellSz - 5, y + 5), 
                                (x + 5, y + self.cellSz - 5), 2)
        
        # Draw misses
        if hasattr(self, 'misses') and self.misses:
            for miss in self.misses:
                row, col = miss
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                # Draw a more visible blue circle
                pygame.draw.circle(self.surface, (0, 0, 255), 
                                  (x + self.cellSz // 2, y + self.cellSz // 2), 
                                  self.cellSz // 3, 0)  # Filled
                # White border for better contrast
                pygame.draw.circle(self.surface, (255, 255, 255), 
                                  (x + self.cellSz // 2, y + self.cellSz // 2), 
                                  self.cellSz // 3, 2)  # Border

    def draw_coordinates(self, offset_x, offset_y):
        # Draw row names (A-J)
        for row in range(self.gridSz):
            row_label = self.coord_font.render(chr(65 + row), True, (255, 255, 255))
            self.surface.blit(row_label, (offset_x - 20, offset_y + row * self.cellSz + self.cellSz // 2 - 5))
        
        # Draw column names (1-10)
        for col in range(self.gridSz):
            col_label = self.coord_font.render(str(col + 1), True, (255, 255, 255))
            self.surface.blit(col_label, (offset_x + col * self.cellSz + self.cellSz // 2 - 5, offset_y - 20))

    def draw_coordinates_button(self):
        # Draw coordinate format
        format_text = self.font.render("Format: A1 or B5", True, (255, 255, 255))
        self.surface.blit(format_text, (self.btncoords.x + 5, self.btncoords.y - 20))

        # Button color based on whether it's active or not
        self.color = self.colorA if self.active else self.colorI
       
        # Draw the coordinates button
        pygame.draw.rect(self.surface, self.color, self.btncoords, 2)
        
        # Button text
        if self.active:
            # If active, show the entered text with a blinking cursor
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            button_text = self.input_text + cursor
        else:
            button_text = "Enter coordinates"
        
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.btncoords.center)
        self.surface.blit(text_surface, text_rect)

    def draw_name_ships(self):
        ship_names = ["Aircraft Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        ship_name_rects = []  # Lista para almacenar los rectángulos de los nombres
        name_positions_y = []
        y_offset = -10
        
        # Actualizar el conteo de barcos hundidos
        ships_sunk = 0
        if self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
        
        for i, name in enumerate(ship_names):
            # Determinar si el barco está hundido
            is_sunk = False
            if self.opponent and i < len(self.opponent.ships):
                is_sunk = self.opponent.ships[i].check_sunken_ship()
            
            # Color del texto: gris si está hundido, blanco si no
            text_color = (150, 150, 150) if is_sunk else (255, 255, 255)
            
            # Renderizar el nombre del barco
            text_surface = self.font.render(name, True, text_color)
            
            # Posición del texto
            text_pos = (self.btncoords.x - 530, self.btncoords.y + y_offset)
            
            # Crear un rectángulo para detectar clics
            text_rect = pygame.Rect(text_pos[0], text_pos[1], text_surface.get_width(), text_surface.get_height())
            ship_name_rects.append((text_rect, i))
            
            # Dibujar el texto si no hay un barco seleccionado
            if not self.selected_ship:
                self.surface.blit(text_surface, text_pos)
                
                # Dibujar una línea a través del nombre si está hundido
                if is_sunk:
                    pygame.draw.line(self.surface, (150, 150, 150),
                                (text_pos[0], text_pos[1] + text_surface.get_height() // 2),
                                (text_pos[0] + text_surface.get_width(), text_pos[1] + text_surface.get_height() // 2),
                                2)
            
            name_positions_y.append(self.btncoords.y + y_offset + self.font.get_linesize() // 2)
            y_offset += 20
        
        # Mostrar el conteo de barcos hundidos
        if self.opponent:
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (self.width - status_text.get_width() - 20, 545))
        
        return name_positions_y, ship_name_rects

    def draw_confirmation_dialog(self):
       # Background of the box
        pygame.draw.rect(self.surface, (0, 0, 0), (200, 200, 400, 200))
        pygame.draw.rect(self.surface, (255, 255, 255), (200, 200, 400, 200), 2)

        # Text
        text = self.font.render("Are you sure about your positions?", True, (255, 255, 255))
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 230))

        # Buttons
        pygame.draw.rect(self.surface, (0, 200, 0), self.btnConfirmYes)
        pygame.draw.rect(self.surface, (200, 0, 0), self.btnConfirmNo)

        yes_text = self.font.render("Yes", True, (255, 255, 255))
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

        # Draw coordinates for the position grid
        self.draw_coordinates(self.offset_x, self.offset_y)

        has_collisions = self.has_ship_collisions()

        # Draw ships
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)

        # Draw buttons
        button_color = (100, 100, 100) if has_collisions else (0, 200, 0)
        pygame.draw.rect(self.surface, button_color, self.btnContinue)

        textContinue = self.font.render('Continue', True, (255, 255, 255))
        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        self.surface.blit(textContinue, rectContinue)

        # Instructions
        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

        if has_collisions:
            warning = self.font.render('Ships are overlapping! Reposition them.', True, (255, 255, 0))
            self.surface.blit(warning, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 40))

        if self.show_confirmation:
            self.draw_confirmation_dialog()

        if hasattr(self, 'status_message') and pygame.time.get_ticks() < self.status_timer:
            status = self.font.render(self.status_message, True, self.status_color)
            # Corrected: proper position for the status message
            self.surface.blit(status, (self.width // 2 - status.get_width() // 2, 550))
        
    def draw_playing(self):
        # Draw position grid
        titlePosit = self.font.render('POSITIONS', True, (255, 255, 255))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 50))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                # Draw damaged positions (where there was a ship but it moved)
                if (row, col) in self.damaged_positions and (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.circle(self.surface, (150, 150, 150),
                                    (x + self.cellSz // 2, y + self.cellSz // 2),
                                    self.cellSz // 3,
                                    3)

        # Draw coordinates for the position grid
        self.draw_coordinates(self.offset_x1, self.offset_y1)

        # Draw ships
        for ship in self.player.ships:
            is_selected = (ship == self.selected_ship)
            
            # Draw each segment of the ship
            for i, pos in enumerate(ship.position):
                row, col = pos
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                
                # Color based on state: damaged, selected, or normal
                if ship.damage_positions[i]:
                    color = (255, 0, 0)
                elif is_selected:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 0)
                    
                pygame.draw.rect(self.surface, color, rect)

        # Draw attack grid
        titleAttck = self.font.render('ATTACK', True, (255, 255, 255))
        self.surface.blit(titleAttck, (self.offset_x2 + 120, self.offset_y2 - 50))

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

        # Draw coordinates for the attack grid
        self.draw_coordinates(self.offset_x2, self.offset_y2)

        # Draw end turn button
        button_color = (255, 0, 0) if self.action_taken else (100, 100, 100)
        pygame.draw.rect(self.surface, button_color, self.btnEndTurn)

        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)
        self.surface.blit(textEndTurn, rectEndTurn)

        # Draw coordinates button
        self.draw_coordinates_button()
        
        # Draw ship names and get their positions
        ship_name_positions_y, ship_name_rects = self.draw_name_ships()

        # Draw movement buttons if a ship is selected and no action has been taken
        if self.selected_ship and not self.action_taken and self.state == "playing":
            # Up button
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveUp)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                            [(60 + 20, 450 + 10), (60 + 10, 450 + 30), (60 + 30, 450 + 30)])
            
            # Down button
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveDown)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                            [(60 + 20, 550 + 30), (60 + 10, 550 + 10), (60 + 30, 550 + 10)])
            
            # Left button
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveLeft)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                            [(20 + 10, 500 + 20), (20 + 30, 500 + 10), (20 + 30, 500 + 30)])
            
            # Right button
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveRight)
            pygame.draw.polygon(self.surface, (255, 255, 255), 
                            [(100 + 30, 500 + 20), (100 + 10, 500 + 10), (100 + 10, 500 + 30)])
            
            # Instructions for moving ships
            move_text = self.font.render("Move ship", True, (255, 255, 255))
            self.surface.blit(move_text, (20, 430))
            
            # Show selected ship name
            selected_ship_text = self.font.render(f"Selected: {self.selected_ship.name}", True, (0, 255, 0))
            self.surface.blit(selected_ship_text, (20, 400))

        # Display turn status - Repositioned to not be stuck to the button
        if self.action_taken:
            if self.shot_made:
                turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
            else:
                turn_status = self.font.render("Ship moved! Click End Turn", True, (255, 255, 0))
            # Position higher to separate from button
            self.surface.blit(turn_status, (300, 420))
        elif not self.action_taken and self.error_message:
            turn_status = self.font.render(self.error_message, True, (255, 0, 0))
            self.surface.blit(turn_status, (300, 420))
        else:
            turn_status = self.font.render("Move a ship or make a shot", True, (255, 255, 255))
            self.surface.blit(turn_status, (300, 420))
    def draw_game_over(self):
        self.state = "game_over"
        self.title = "GAME OVER"

        textReset = self.font.render('RESTART GAME', True, (255, 255, 255))
        rectReset = textReset.get_rect(center=self.btnReset.center)
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset)
        self.surface.blit(textReset, rectReset)

        game_over_text = self.font.render(f"{self.winner} WINS!", True, (255, 255, 0))
        message_win = game_over_text.get_rect(center=(self.width // 2, 300))
        self.surface.blit(game_over_text, message_win)

    def handle_events(self, events):
        if self.state == "setup":
            # Process all MOUSEBUTTONUP events first to ensure dragging state is reset
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Force end dragging for all ships to ensure clean state
                    for ship in self.ships:
                        if ship.dragging:
                            ship.end_drag(self.gridSz, self.ships)
                        # Force reset dragging state for all ships
                        ship.dragging = False
                        ship.mouse_down_pos = None
            
            # Find any ship that is currently being dragged
            currently_dragging = None
            for ship in self.ships:
                if ship.dragging:
                    currently_dragging = ship
                    break
            
            # Now process other events
            for event in events:
                # Skip MOUSEBUTTONUP events as we've already processed them
                if event.type == pygame.MOUSEBUTTONUP:
                    continue
                    
                # If a ship is already being dragged, only process events for that ship
                if currently_dragging:
                    currently_dragging.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz, self.ships)
                else:
                    # If no ship is being dragged, check if we should start dragging one
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for ship in self.ships:
                            if ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz, self.ships):
                                # This ship started dragging, don't process for other ships
                                break
        
        elif self.state == "playing":
            for event in events:   
                mouse_pos = pygame.mouse.get_pos()    
                if not self.action_taken:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btncoords.collidepoint(mouse_pos):
                            self.active = True
                            # Clear error message when clicking on the field
                            self.error_message = ""
                            # Force update to show the active state immediately
                            self.force_update()
                        else:
                            if self.active:  # Solo desactivar si estaba activo
                                self.active = False
                                # Force update to show the inactive state immediately
                                self.force_update()
                    
                    # Handle keyboard events when the field is active
                    if event.type == pygame.KEYDOWN and self.active:
                        if event.key == pygame.K_RETURN:
                            # Process the attack when Enter is pressed
                            logger.debug("[INPUT] Enter key pressed, processing attack input")
                            result = self.handle_attack_input(self.input_text)
                            self.input_text = ""
                            # Force update to show results immediately
                            self.force_update()
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                            # Force update to show text changes immediately
                            self.force_update()
                        elif event.key == pygame.K_ESCAPE:
                            # Allow canceling input with ESC
                            self.active = False
                            self.input_text = ""
                            # Force update to show changes immediately
                            self.force_update()
                        else:
                            # Limit text length and only accept alphanumeric characters
                            if len(self.input_text) < 3 and event.unicode.isalnum():
                                self.input_text += event.unicode
                                # Force update to show text changes immediately
                                self.force_update()

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
            # If an action has already been taken, only allow ending the turn
            if self.action_taken:
                if self.btnEndTurn.collidepoint(mouse_pos):
                    return "end_turn"
                return None
                
            # Check if movement buttons were clicked
            if self.selected_ship:
                if self.btnMoveUp.collidepoint(mouse_pos):
                    return self.move_selected_ship('up')
                elif self.btnMoveDown.collidepoint(mouse_pos):
                    return self.move_selected_ship('down')
                elif self.btnMoveLeft.collidepoint(mouse_pos):
                    return self.move_selected_ship('left')
                elif self.btnMoveRight.collidepoint(mouse_pos):
                    return self.move_selected_ship('right')
            
            # Check if a ship name was clicked
            _, ship_name_rects = self.draw_name_ships()
            for rect, ship_index in ship_name_rects:
                if rect.collidepoint(mouse_pos) and ship_index < len(self.player.ships):
                    # If already selected, deselect it
                    if self.selected_ship == self.player.ships[ship_index]:
                        self.selected_ship = None
                    else:
                        self.selected_ship = self.player.ships[ship_index]
                    return "ship_selected"
            
            # Check if a ship was clicked on the position board
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x1 + col * self.cellSz
                    y = self.offset_y1 + row * self.cellSz
                    position_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    
                    if position_rect.collidepoint(mouse_pos):
                        return self.handle_ship_selection(row, col)
            
            # Check if the attack board was clicked
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        # Deselect ship when attacking
                        self.selected_ship = None
                        return self.handle_attack(mouse_pos, row, col)

            # Check if end turn button was clicked
            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.action_taken or self.game_over:
                    # Deselect ship when ending turn
                    self.selected_ship = None
                    return "end_turn"
        return None
    
    def handle_ship_selection(self, row, col):
        # Check if there's a ship at the selected position
        for ship in self.player.ships:
            if (row, col) in ship.position:
                # If already selected, deselect it
                if self.selected_ship == ship:
                    self.selected_ship = None
                else:
                    self.selected_ship = ship
                return "ship_selected"
        
        # If no ship, deselect
        self.selected_ship = None
        return None
    
    def move_selected_ship(self, direction):
        if not self.selected_ship or self.action_taken:
            return None

        # Check if the ship can be moved according to damage rules
        if not self.can_ship_move(self.selected_ship):
            self.collision_message = "Engine damage. Cannot move"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None
    
        # Save the current positions of the ship before moving it
        old_positions = self.selected_ship.position.copy()
        
        # Check if the ship can move in that direction
        if self.selected_ship.can_move(direction, self.gridSz, self.player.ships):
            # Record damaged positions before moving
            for idx, pos in enumerate(old_positions):
                if self.selected_ship.damage_positions[idx]:
                    self.damaged_positions.add(pos)
            
            # Move the ship
            self.selected_ship.move(direction)
    
            # Update the player's board
            self.update_player_board()
            
            # Mark that an action has been taken
            self.action_taken = True
            
            # Send movement message to opponent if connected
            if self.connection and self.connection.connected:
                try:
                    ship_index = self.player.ships.index(self.selected_ship)
                    self.connection.enviar_datos({
                        "type": "ship_moved",
                        "ship_index": ship_index,
                        "direction": direction
                    })
                    logger.debug(f"[MOVE] Sent movement message: ship {ship_index}, direction {direction}")
                except Exception as e:
                    logger.exception("[MOVE] Error sending movement message")
            
            return "ship_moved"
        else:
            # Show message that the ship cannot move
            self.collision_message = "Ship cannot move in this direction"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None
    
    def can_ship_move(self, ship):
        if ship.life == ship.length:
            return True
            
        # For ships of length 1, they cannot move if damaged
        if ship.length == 1:
            return False
            
        # For longer ships, check if damage is in internal positions
        for idx in range(1, ship.length - 1):  # Internal positions (1 to length-2)
            if ship.damage_positions[idx]:
                return False  # Cannot move if there is damage in internal positions
            
        # If only damage is at the ends, it can move
        return True
    
    def update_player_board(self):
        # Clear the board
        self.player.board.grid = [['w' for _ in range(self.player.board.size)] for _ in range(self.player.board.size)]
        
        # Mark missed shot positions as 'o'
        if hasattr(self.opponent, 'misses'):
            for row, col in self.opponent.misses:
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Only mark as 'o' if there is no ship at that position
                    if (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                        self.player.board.grid[row][col] = 'o'
        
        # Update ship positions on the board
        for ship in self.player.ships:
            for idx, (row, col) in enumerate(ship.position):
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Mark as 's' if not damaged, or as 'x' if damaged
                    if ship.damage_positions[idx]:
                        self.player.board.grid[row][col] = 'x'  # Damaged part of the ship
                    else:
                        self.player.board.grid[row][col] = 's'  # Intact part of the ship

    def handle_attack_input(self, input_text):
        logger = logging.getLogger(__name__)
        logger.debug(f"[ATTACK_INPUT] Processing input: '{input_text}'")
        
        self.error_message = ""
        
        # Trim whitespace and convert to uppercase
        input_text = input_text.strip().upper()
        
        # Validate that the input has at least 2 characters
        if len(input_text) < 2:
            self.error_message = "Invalid format! Example: A1, B5"
            self.active = False
            logger.debug(f"[ATTACK_INPUT] Error: {self.error_message}")
            return self.error_message

        # Validate that the first character is a letter A-J
        if not input_text[0].isalpha() or input_text[0] not in "ABCDEFGHIJ":
            self.error_message = "First character must be a letter A-J!"
            self.active = False
            logger.debug(f"[ATTACK_INPUT] Error: {self.error_message}")
            return self.error_message

        # Extract the numeric part (can be more than one digit)
        letter_part = input_text[0]
        number_part = input_text[1:]
        
        # Validate that the numeric part is a number
        if not number_part.isdigit():
            self.error_message = "Numeric part must be a number!"
            self.active = False
            logger.debug(f"[ATTACK_INPUT] Error: {self.error_message}")
            return self.error_message
        
        # Convert to coordinates
        row = ord(letter_part) - ord('A')
        col = int(number_part) - 1
        
        logger.debug(f"[ATTACK_INPUT] Converted to coordinates: ({row}, {col})")
        
        # Check if coordinates are within bounds
        if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
            # Call handle_attack with the coordinates
            logger.debug(f"[ATTACK_INPUT] Calling handle_attack with coordinates: ({row}, {col})")
            result = self.handle_attack(None, row, col)
            if result == "shot_made":
                self.action_taken = True
                self.active = False
                logger.debug("[ATTACK_INPUT] Shot made successfully")
                return "shot_made"
            else:
                self.error_message = "Could not make the shot. Try again."
                self.active = False
                logger.debug(f"[ATTACK_INPUT] Error: {self.error_message}")
                return self.error_message
        else:
            self.error_message = "Coordinates out of bounds!"
            self.active = False
            logger.debug(f"[ATTACK_INPUT] Error: {self.error_message}")
            return self.error_message

    def handle_attack(self, mouse_pos, row, col):
        logger = logging.getLogger(__name__)
        logger.debug(f"[ATTACK] Attempting to attack ({row},{col})")

        if not self.connection or not self.connection.connected:
            logger.error("[ATTACK] Connection closed.")
            return None

        if self.action_taken:
            logger.warning("[ATTACK] You already took an action this turn.")
            return None

        if self.game_over:
            logger.warning("[ATTACK] The game is over.")
            return None

        if (row, col) in self.hits or (row, col) in self.misses:
            if not self.option_allow_reshoot:
                logger.info(f"[ATTACK] You already shot at ({row},{col}) before.")
                return None
            else:
                # Check if there's a ship at the position
                has_ship = False
                ship_already_damaged = False
                for ship in self.opponent.ships:
                    if (row, col) in ship.position:
                        has_ship = True
                        position_index = ship.position.index((row, col))
                        if position_index >= 0 and ship.damage_positions[position_index]:
                            ship_already_damaged = True
                        break
                
                # If there's a ship, the position is in misses, and that part of the ship is NOT damaged, allow re-attack
                if has_ship and (row, col) in self.misses and not ship_already_damaged:
                    # Remove from misses list since it will now be a hit
                    self.misses.remove((row, col))
                # If there's no ship, it's already a hit, or that part of the ship is already damaged, don't allow re-attack
                elif (row, col) in self.hits or (row, col) in self.misses:
                    return None

        try:
            # Send the attack
            self.connection.enviar_datos({"type": "attack", "row": row, "col": col})
            logger.debug("[ATTACK] Attack sent successfully.")
            
            # Mark that a shot has been made this turn
            self.shot_made = True
            self.action_taken = True
            
            # Update the interface to show waiting for response
            self.status_message = "Waiting for result..."
            self.status_timer = pygame.time.get_ticks() + 5000
            self.status_color = (255, 255, 0)
            
            # Force screen update
            self.force_update()
            
            self.debug_state()
            return "shot_made"
        except Exception as e:
            logger.exception("[ATTACK] Exception during attack.")
            return None

    def wait_for_opponent_turn(self):
        logger = logging.getLogger(__name__)

        if not self.connection or not hasattr(self.connection, "canal"):
            logger.error("[WAIT] No active connection or channel not available.")
            self.status_message = "Connection not available."
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            self._cerrar_por_desconexion("Invalid channel in connection.")
            return

        try:
            # Reducir el tiempo de espera de select para mayor responsividad
            ready, _, _ = select.select([self.connection.canal], [], [], 0.05)
            if ready:
                datos = self.connection.canal.recv(self.connection.bufsize).decode("utf-8")
                if not datos:
                    logger.error("[WAIT] Socket was closed by the other end.")
                    self._cerrar_por_desconexion("Socket closed unexpectedly.")
                    return

                self._recv_buffer += datos
                while '\n' in self._recv_buffer:
                    raw, self._recv_buffer = self._recv_buffer.split('\n', 1)
                    try:
                        msg = json.loads(raw)
                        self._procesar_mensaje_red(msg)
                    except json.JSONDecodeError as e:
                        logger.warning(f"[WAIT] Invalid JSON received: {e}")

            # Actualizar el mensaje de estado periódicamente para mostrar que el juego sigue activo
            current_time = pygame.time.get_ticks()
            if current_time % 3000 < 50:  # Actualizar aproximadamente cada 3 segundos
                self.status_message = "Waiting for opponent's move..."
                self.status_timer = current_time + 3000
                self.status_color = (255, 255, 0)
                self.force_update()  # Forzar actualización para mostrar el mensaje

        except Exception as e:
            logger.error(f"[WAIT] Error in select/recv: {e}")
            self.status_message = "Network error"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            self._cerrar_por_desconexion(f"Network error: {e}")
        
        # Asegurar que los hits y misses se muestren correctamente
        if self.hits or self.misses:
            self.draw()
            pygame.display.update()

    def _procesar_mensaje_red(self, msg):
        logger = logging.getLogger(__name__)
        logger.debug(f"[NET] Message received: {msg}")

        if not isinstance(msg, dict) or "type" not in msg:
            logger.warning("[NET] Invalid message received: %s", msg)
            return

        if msg["type"] == "ping":
            self.connection.enviar_datos({"type": "pong"})

        elif msg["type"] == "turn_ready":
            logger.debug("[NET] Turn received, it's your turn now.")
            self.switch_to_playing()
            # Set turn message only once
            self.status_message = "It's your turn"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (0, 255, 0)

        elif msg["type"] == "turn_complete":
            logger.debug("[NET] Opponent's turn finished. It's your turn now.")
            self.switch_to_playing()
            # Set turn message only once
            self.status_message = "It's your turn"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (0, 255, 0)

        elif msg["type"] == "attack":
            if not all(k in msg for k in ("row", "col")):
                logger.warning("[NET] Incomplete 'attack' packet.")
                return

            row, col = msg["row"], msg["col"]
            logger.debug(f"[NET] Attack received at ({row},{col})")

            if not self.player or not self.opponent:
                logger.error("[NET] Invalid state, player or opponent is None.")
                self._cerrar_por_desconexion("Invalid state.")
                return

            try:
                # Correctly use the shoot_at_opponent method
                # The current player (self.player) shoots at the opponent (self.opponent)
                result = self.opponent.shoot_at_opponent(self.player, row, col)
                logger.debug(f"[NET] Shot result: {result}")

                self.connection.enviar_datos({
                    "type": "result",
                    "result": result,
                    "row": row,
                    "col": col
                })

                # Check if all ships are sunk after the attack
                victory = self.player.all_ships_sunken()
                if victory:
                    logger.debug("[VICTORY] All player ships have been sunk")
                    self.game_over = True
                    self.winner = f"Player {3 - self.player_number}"  # Opponent wins
                    self.connection.enviar_datos({
                        "type": "victory",
                        "winner": 3 - self.player_number
                    })
                    # Force update to show game over screen immediately
                    self.force_update()
                else:
                    self.shot_made = False
                    self.state = "waiting_for_opponent"

            except Exception as e:
                logger.exception("[NET] Error processing attack")

        elif msg["type"] == "result":
            logger.debug(f"[RESULT] Result received: {msg}")
            row, col = msg.get("row"), msg.get("col")
            result = msg.get("result")

            if row is None or col is None:
                logger.warning("[RESULT] Missing coordinate in result message.")
                return

            if result == "Disparo exitoso":
                if (row, col) not in self.hits:
                    self.hits.append((row, col))
                    self.last_result_message = "X Hit!"
                    
                    # Check if this hit sunk a ship
                    for ship in self.opponent.ships:
                        if (row, col) in ship.position:
                            position_index = ship.position.index((row, col))
                            ship.damage_positions[position_index] = True
                            ship.life -= 1
                            
                            # Check if ship is now sunk
                            if ship.life <= 0:
                                self.status_message = f"You sunk their {ship.name}!"
                                self.status_timer = pygame.time.get_ticks() + 3000
                                self.status_color = (255, 255, 0)
                            break
            else:
                if (row, col) not in self.misses:
                    self.misses.append((row, col))
                    self.last_result_message = "O Miss"

            self.last_result_time = pygame.time.get_ticks()
            self.shot_made = True
            logger.debug(f"[RESULT] Updated hits/misses: {self.hits=} {self.misses=}")
            
            # Check for victory after processing the result
            all_sunk = all(ship.check_sunken_ship() for ship in self.opponent.ships)
            if all_sunk:
                logger.debug("[VICTORY] All opponent ships have been sunk")
                self.game_over = True
                self.winner = f"Player {self.player_number}"  # You win
                self.connection.enviar_datos({
                    "type": "victory",
                    "winner": self.player_number
                })
            
            # Force update to show the result immediately
            self.force_update()

        elif msg["type"] == "victory":
            self.game_over = True
            self.winner = f"Player {msg['winner']}"
            self.state = "game_over"
            logger.info(f"[VICTORY] The winner is Player {msg['winner']}")
            # Force update to show game over screen immediately
            self.force_update()

        elif msg["type"] == "ship_moved":
            # Process opponent ship movement
            if not all(k in msg for k in ("ship_index", "direction")):
                logger.warning("[NET] Incomplete 'ship_moved' packet.")
                return
                
            ship_index = msg["ship_index"]
            direction = msg["direction"]
            
            if not self.opponent or ship_index >= len(self.opponent.ships):
                logger.error(f"[NET] Invalid ship index: {ship_index}")
                return
                
            ship = self.opponent.ships[ship_index]
            
            # Save old positions to update hits/misses
            old_positions = ship.position.copy()
            
            # Move opponent's ship
            if ship.can_move(direction, self.gridSz, self.opponent.ships):
                ship.move(direction)
                logger.debug(f"[NET] Opponent's ship {ship_index} moved in direction {direction}")
                
                # Update opponent's board
                self.opponent.update_board()
                
                # Show movement message
                # Translate direction to English
                dir_en = direction
                self.status_message = f"Opponent moved a ship {dir_en}"
                self.status_timer = pygame.time.get_ticks() + 3000
                self.status_color = (255, 255, 0)
                
                # Force update to show the movement immediately
                self.force_update()
            else:
                logger.warning(f"[NET] Could not move ship {ship_index} in direction {direction}")

    def end_turn(self):
        logger = logging.getLogger(__name__)

        if not self.connection or not self.connection.connected:
            logger.warning("[END TURN] No active connection.")
            return

        if not self.action_taken:
            logger.warning("[END TURN] Attempt to end turn without taking action.")
            self.status_message = "You must make a shot or move a ship first!"
            self.status_timer = pygame.time.get_ticks() + 3000
            self.status_color = (255, 0, 0)
            return

        try:
            logger.debug("[END TURN] Sending 'turn_complete' to opponent...")
            self.connection.enviar_datos({"type": "turn_complete"})

            # Change local state
            self.state = "waiting_for_opponent"
            self.shot_made = False
            self.action_taken = False
            self.selected_ship = None

            # On-screen message in English
            self.status_message = "Waiting for opponent's turn..."
            self.status_color = (255, 255, 0)
            self.status_timer = pygame.time.get_ticks() + 5000

            logger.debug("[END TURN] Turn ended, waiting for opponent.")

        except Exception as e:
            logger.exception("[END TURN] Error ending turn.")
            self.status_message = "Network error ending turn."
            self.status_color = (255, 0, 0)
            self.status_timer = pygame.time.get_ticks() + 5000
        
    def _cerrar_por_desconexion(self, motivo="Disconnection"):
        self.state = "disconnected"
        self.game_over = True
        self.winner = motivo
        self.status_message = motivo
        self.status_timer = pygame.time.get_ticks() + 5000

    def reset_shot_flag(self):
        self.shot_made = False
        self.action_taken = False
        self.selected_ship = None

    def debug_state(self):
        """Prints the current game state for debugging"""
        logger = logging.getLogger(__name__)
        logger.debug("=== GAME STATE ===")
        logger.debug(f"State: {self.state}")
        logger.debug(f"Shot made: {self.shot_made}")
        logger.debug(f"Action taken: {self.action_taken}")
        logger.debug(f"Selected ship: {self.selected_ship}")
        logger.debug(f"Hits: {self.hits}")
        logger.debug(f"Misses: {self.misses}")
        logger.debug(f"Last result: {self.last_result_message}")
        logger.debug("=====================")

    def force_update(self):
        """Forces a complete screen update"""
        self.draw()
        pygame.display.update()
        logger.debug("[UPDATE] Forcing screen update")

    def procesar_resultado(self, row, col, resultado):
        """Directly processes an attack result and updates the interface"""
        logger = logging.getLogger(__name__)
        
        # Convert to integers if necessary
        try:
            row = int(row)
            col = int(col)
        except (TypeError, ValueError):
            logger.error(f"[RESULT] Invalid values for row/col: {row}/{col}")
            return
        
        # Initialize arrays if they don't exist
        if not hasattr(self, 'hits') or self.hits is None:
            self.hits = []
        if not hasattr(self, 'misses') or self.misses is None:
            self.misses = []
        
        # Update arrays and messages
        if resultado == "Disparo exitoso":
            if (row, col) not in self.hits:
                self.hits.append((row, col))
                logger.debug(f"[RESULT] Added hit at ({row},{col}). Current hits: {self.hits}")
        else:
            if (row, col) not in self.misses:
                self.misses.append((row, col))
                logger.debug(f"[RESULT] Added miss at ({row},{col}). Current misses: {self.misses}")
        
        # Update messages
        self.last_result_message = "X Hit!" if resultado == "Disparo exitoso" else "O Miss"
        self.last_result_time = pygame.time.get_ticks()
        self.status_message = self.last_result_message
        self.status_color = (0, 255, 0) if "Hit!" in self.last_result_message else (255, 255, 0)
        self.status_timer = pygame.time.get_ticks() + 3000
        
        # Force redraw
        self.draw()
        pygame.display.update()
        logger.debug(f"[RESULT] Result processed and drawn: {self.last_result_message} at ({row},{col})")
        self.debug_state()