import pygame

class Ship:
    def __init__(self, length, x, y, isHorizontal=True, name=None):
        self.length = length
        self.x = x
        self.y = y
        self.life = length
        self.isHorizontal = isHorizontal
        self.name = name or f"Ship{length}"
        self.position = self._calculate_positions()
        
        # UI properties
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.is_colliding = False
    
    def _calculate_positions(self):
        positions = []
        if self.isHorizontal:
            for i in range(self.length):
                positions.append((int(self.y), int(self.x) + i))
        else:
            for i in range(self.length):
                positions.append((int(self.y) + i, int(self.x)))
        return positions
    
    def update_positions(self):
        self.position = self._calculate_positions()
    
    def check_sunken_ship(self):
        return self.life == 0
    
    def damage_received_ship(self):
        if self.life > 0:
            self.life -= 1
    
    def check_collision(self, other_ships):

        my_positions = set(self.position)
        
        for other_ship in other_ships:
          
            if self == other_ship:
                continue

            other_positions = set(other_ship.position)
            
            if my_positions.intersection(other_positions):
                return True
                
        return False
    
    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10, other_ships=None):
        if other_ships is None:
            other_ships = []
        
        original_x, original_y = self.x, self.y
        original_horizontal = self.isHorizontal
        original_positions = self.position.copy()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            if self.isHorizontal:
                ship_rect = pygame.Rect(
                    offset_x + self.x * cellSize,
                    offset_y + self.y * cellSize,
                    self.length * cellSize,
                    cellSize
                )
            else:
                ship_rect = pygame.Rect(
                    offset_x + self.x * cellSize,
                    offset_y + self.y * cellSize,
                    cellSize,
                    self.length * cellSize
                )
                    
            if ship_rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                self.offset_x = self.x * cellSize - (mouse_x - offset_x)
                self.offset_y = self.y * cellSize - (mouse_y - offset_y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                
                self.x = round((self.x * cellSize) / cellSize)
                self.y = round((self.y * cellSize) / cellSize)
                
                if self.isHorizontal:
                    self.x = max(0, min(gridSize - self.length, self.x))
                    self.y = max(0, min(gridSize - 1, self.y))
                else:
                    self.x = max(0, min(gridSize - 1, self.x))
                    self.y = max(0, min(gridSize - self.length, self.y))
                
                self.update_positions()
                
                if other_ships and self.check_collision(other_ships):
                    self.x, self.y = original_x, original_y
                    self.isHorizontal = original_horizontal
                    self.position = original_positions
                    self.is_colliding = True
                else:
                    self.is_colliding = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos

            newX = (mouse_x - offset_x + self.offset_x) / cellSize
            newY = (mouse_y - offset_y + self.offset_y) / cellSize
            
            if self.isHorizontal:
                self.x = max(0, min(gridSize - self.length, newX))
                self.y = max(0, min(gridSize - 1, newY))
            else:
                self.x = max(0, min(gridSize - 1, newX))
                self.y = max(0, min(gridSize - self.length, newY))
            
            self.update_positions()
            
            if other_ships:
                self.is_colliding = self.check_collision(other_ships)
        
        elif event.type == pygame.KEYDOWN and self.dragging and event.key == pygame.K_SPACE:
            
            original_horizontal = self.isHorizontal
            original_x, original_y = self.x, self.y
        
            self.rotate(gridSize)
            self.update_positions()
            
            if other_ships and self.check_collision(other_ships):
                self.isHorizontal = original_horizontal
                self.x, self.y = original_x, original_y
                self.update_positions()
                self.is_colliding = True
            else:
                self.is_colliding = False

    def rotate(self, gridSize):
        if self.isHorizontal:
            center_x = self.x + self.length / 2
            center_y = self.y + 0.5
        else:
            center_x = self.x + 0.5
            center_y = self.y + self.length / 2
       
        self.isHorizontal = not self.isHorizontal
        
        if self.isHorizontal:
            newX = center_x - self.length / 2
            newY = center_y - 0.5
        else:
            newX = center_x - 0.5
            newY = center_y - self.length / 2

        if self.isHorizontal:
            self.x = max(0, min(gridSize - self.length, newX))
            self.y = max(0, min(gridSize - 1, newY))
        else:
            self.x = max(0, min(gridSize - 1, newX))
            self.y = max(0, min(gridSize - self.length, newY))

    def draw(self, surface, offset_x, offset_y, cellSize):

        color = (255, 0, 0) if self.is_colliding else (0, 0, 0)
        
        if self.isHorizontal:
            for i in range(self.length):
                x = offset_x + (self.x + i) * cellSize
                y = offset_y + self.y * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(surface, color, rect)
        else:
            for i in range(self.length):
                x = offset_x + self.x * cellSize
                y = offset_y + (self.y + i) * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(surface, color, rect)