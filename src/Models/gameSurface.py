import pygame
from src.Models.board import Board
from src.Game.player import Player
from src.Game.gameLogic import GameLogic
from src.Models.ship import Ship

class GameSurface:
    def __init__(self, title, width, height):
        pygame.font.init()
        self.width = width
        self.height = height
        self.title = title
        self.surface = pygame.Surface((width, height))
        self.surface.fill((0, 128, 255))
        
        self.gridSz = 10
        self.cellSz = 30
        self.offset_x = 250
        self.offset_y = 100
        
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
        self.btnContinue = pygame.Rect(250, 545, 90, 50)
        self.btnReset = pygame.Rect(340, 400, 120, 50)
        self.btnEndTurn = pygame.Rect(350, 500, 90, 50)
        
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
        self.surface.fill((0, 128, 255))
        
        # Draw title
        title = self.font.render(self.title, True, (255, 255, 255))
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
            self.surface.blit(message, (self.width // 2 - message.get_width() // 2, 500))
    
    def draw_setup(self):
        # Draw grid
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
    
        has_collisions = self.has_ship_collisions()
        
        # Draw ships
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)
        
        # Draw buttons
        button_color = (100, 100, 100) if has_collisions else (255, 0, 0)
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
    
    def draw_playing(self):
        # Draw position grid
        titlePosit = self.font.render('POSITIONS', True, (0, 0, 0))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 40))
        
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                
                # Draw ships
                if self.player and (row, col) in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.rect(self.surface, (0, 0, 0), rect)
        
        # Draw attack grid
        titleAttck = self.font.render('ATTACK', True, (0, 0, 0))
        self.surface.blit(titleAttck, (self.offset_x2 + 120, self.offset_y2 - 40))
        
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                
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
        button_color = (255, 0, 0) if self.shot_made else (100, 100, 100)
        pygame.draw.rect(self.surface, button_color, self.btnEndTurn)
        
        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)
        self.surface.blit(textEndTurn, rectEndTurn)
        
        # Display game status
        if self.player and self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (600, 545))
            
            # Display turn status
            if self.shot_made:
                turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
                self.surface.blit(turn_status, (300, 450))
            else:
                turn_status = self.font.render("Make your shot", True, (255, 255, 255))
                self.surface.blit(turn_status, (340, 450))
   
    def draw_game_over(self):
        self.title = "Game over"
        title = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 25))
        self.surface.blit(title, title_rect)
        
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
        if self.state == "setup":
            if self.btnContinue.collidepoint(mouse_pos):
                if not self.has_ship_collisions():
                    return "continue"
                else:
                    self.collision_message = "You cannot continue with overlapping ships!"
                    self.message_timer = pygame.time.get_ticks() + 3000 
        else:  # playing state
            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.shot_made or self.game_over:
                    return "end_turn"
            else:
                return self.handle_attack(mouse_pos)
        return None
    
    def handle_attack(self, mouse_pos):
        # Don't allow shooting if a shot has already been made this turn
        if self.shot_made or not self.player or not self.opponent or self.game_over:
            return None
            
        # Check if click is in attack grid
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x2 + col * self.cellSz
                y = self.offset_y2 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                
                if rect.collidepoint(mouse_pos):
                    # Don't allow clicking on already attacked cells
                    if (row, col) in self.hits or (row, col) in self.misses:
                        return None
                    
                    # Use Player class to shoot at opponent
                    result = self.player.shoot_at_opponent(self.opponent, row, col)
                    
                    if result == "Disparo exitoso":
                        self.hits.append((row, col))
                    else:
                        self.misses.append((row, col))
                    
                    # Check for win condition using GameLogic
                    victory_message = self.game_logic.check_victory()
                    if victory_message:
                        self.game_over = True
                        self.winner = f"Player {self.player_number}"
                    
                    # Set the shot_made flag to true
                    self.shot_made = True
                    
                    return "shot_made"
        
        return None
    
    def reset_shot_flag(self):
        self.shot_made = False