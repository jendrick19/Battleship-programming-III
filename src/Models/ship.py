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
        self.damage_positions = [False] * self.length  # Indicates which segments of the ship are damaged
        
        # UI properties
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.is_colliding = False

        # initial Positions for collide check
        self.initial_x = x
        self.initial_y = y
        self.initial_isHorizontal = isHorizontal
    
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
        self.is_colliding = False
    
    def check_sunken_ship(self):
        return self.life <= 0
    
    def damage_received_ship(self, x, y):
        for idx, pos in enumerate(self.position):
            if pos[0] == x and pos[1] == y:
                if not self.damage_positions[idx]:
                    self.damage_positions[idx] = True
                    self.life -= 1
                    return True
        return False
    
    def can_move(self, direction, board, other_ships):
        if self.check_sunken_ship():
            return False 

        # Calculate new positions based on direction
        if direction == 'left' and self.isHorizontal:
            if self.damage_positions[0]:
                return False 
            new_x = self.x - 1
            
            if new_x < 0: 
                return False
            new_pos = [(y, x - 1) for y, x in self.position]
        
        elif direction == 'right' and self.isHorizontal:
            if self.damage_positions[-1]: 
                return False  
            new_x = self.x + 1
            if new_x + self.length > board: 
                return False
            new_pos = [(y, x + 1) for y, x in self.position]
        
        elif direction == 'up' and not self.isHorizontal:
            if self.damage_positions[0]:
                return False
            new_y = self.y - 1
            
            if new_y < 0:
                return False
            new_pos = [(y - 1, x) for y, x in self.position]
        
        elif direction == 'down' and not self.isHorizontal:
            if self.damage_positions[-1]:
                return False
            new_y = self.y + 1
            
            if new_y + self.length > board:
                return False
            new_pos = [(y + 1, x) for y, x in self.position]
        
        else:
            return False
        
        # Check collisions with other ships
        for ship in other_ships:
            if ship == self: continue
            if set(new_pos).intersection(set(ship.position)):
                return False

        return True
    
    def move(self, direction):
        if direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
        elif direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        self.update_positions()
    
    def check_collision(self, other_ships):
        my_positions = set(self.position)
        
        for other_ship in other_ships:
            if self == other_ship:
                continue

            other_positions = set(other_ship.position)
            
            if my_positions.intersection(other_positions):
                return True
                
        return False
    
    def get_rect(self, offset_x, offset_y, cellSize):
        """Get the rectangle that represents the ship's area"""
        if self.isHorizontal:
            return pygame.Rect(
                offset_x + self.x * cellSize,
                offset_y + self.y * cellSize,
                self.length * cellSize,
                cellSize
            )
        else:
            return pygame.Rect(
                offset_x + self.x * cellSize,
                offset_y + self.y * cellSize,
                cellSize,
                self.length * cellSize
            )
    
    def start_drag(self, mouse_x, mouse_y, offset_x, offset_y, cellSize):
        """Start dragging the ship"""
        self.dragging = True
        # Calculate offset from mouse position to ship origin
        self.offset_x = mouse_x - (offset_x + self.x * cellSize)
        self.offset_y = mouse_y - (offset_y + self.y * cellSize)
        # Save initial position for collision handling
        self.initial_x = self.x
        self.initial_y = self.y
        self.initial_isHorizontal = self.isHorizontal
    
    def end_drag(self, gridSize, other_ships):
        """End dragging the ship"""
        if not self.dragging:
            return False
            
        self.dragging = False
        
        # Round to nearest cell position
        self.x = round(self.x)
        self.y = round(self.y)
        
        # Ensure ship is within bounds
        if self.isHorizontal:
            self.x = max(0, min(gridSize - self.length, self.x))
            self.y = max(0, min(gridSize - 1, self.y))
        else:
            self.x = max(0, min(gridSize - 1, self.x))
            self.y = max(0, min(gridSize - self.length, self.y))
        
        self.update_positions()
        
        # Check collisions with other ships
        if other_ships and self.check_collision(other_ships):
            self.is_colliding = True
            self.x = self.initial_x  # if collide, set positions to initial positions
            self.y = self.initial_y
            self.isHorizontal = self.initial_isHorizontal
            self.update_positions()
            return False
        else:
            self.is_colliding = False
            return True
    
    def update_drag_position(self, mouse_x, mouse_y, offset_x, offset_y, cellSize, gridSize):
        """Update the ship's position during dragging"""
        if not self.dragging:
            return False
            
        # Calculate new position based on mouse position and offset
        new_x = (mouse_x - offset_x - self.offset_x) / cellSize
        new_y = (mouse_y - offset_y - self.offset_y) / cellSize
        
        # Update ship position
        self.x = new_x
        self.y = new_y
        
        # Limit position within board boundaries
        if self.isHorizontal:
            self.x = max(0, min(gridSize - self.length, self.x))
            self.y = max(0, min(gridSize - 1, self.y))
        else:
            self.x = max(0, min(gridSize - 1, self.x))
            self.y = max(0, min(gridSize - self.length, self.y))
        
        self.update_positions()
        return True
    
    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10, other_ships=None):
        if other_ships is None:
            other_ships = []
        
        # Handle mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # Check if the mouse click is on the ship
            ship_rect = self.get_rect(offset_x, offset_y, cellSize)
            if ship_rect.collidepoint(mouse_x, mouse_y):
                self.start_drag(mouse_x, mouse_y, offset_x, offset_y, cellSize)
                return True
            
        # Handle mouse button up event
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                result = self.end_drag(gridSize, other_ships)
                return result
        
        # Handle mouse motion event
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            result = self.update_drag_position(mouse_x, mouse_y, offset_x, offset_y, cellSize, gridSize)
            
            # Check collisions in real time
            if result and other_ships:
                self.is_colliding = self.check_collision(other_ships)
            
            return result
        
        # Handle key press event for rotation
        elif event.type == pygame.KEYDOWN and self.dragging and event.key == pygame.K_SPACE:
            # Rotate the ship
            self.rotate(gridSize)
            self.update_positions()
            
            # Check collisions after rotating
            if other_ships and self.check_collision(other_ships):
                self.is_colliding = True
            else:
                self.is_colliding = False
            
            return True
        
        return False

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
        
        # Highlight the ship if it's being dragged
        if self.dragging:
            color = (0, 255, 0)  # Green for dragging
        
        if self.isHorizontal:
            for i in range(self.length):
                x = offset_x + (self.x + i) * cellSize
                y = offset_y + self.y * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                
                # Draw the ship segment
                segment_color = (255, 0, 0) if self.damage_positions[i] else color
                pygame.draw.rect(surface, segment_color, rect)
        else:
            for i in range(self.length):
                x = offset_x + self.x * cellSize
                y = offset_y + (self.y + i) * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                
                # Draw the ship segment
                segment_color = (255, 0, 0) if self.damage_positions[i] else color
                pygame.draw.rect(surface, segment_color, rect)