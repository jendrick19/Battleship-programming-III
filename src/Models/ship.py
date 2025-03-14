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
    
    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10):
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
    
        elif event.type == pygame.KEYDOWN and self.dragging and event.key == pygame.K_SPACE:
            self.rotate(gridSize)
            self.update_positions()

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
        if self.isHorizontal:
            for i in range(self.length):
                x = offset_x + (self.x + i) * cellSize
                y = offset_y + self.y * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(surface, (0, 0, 0), rect)
        else:
            for i in range(self.length):
                x = offset_x + self.x * cellSize
                y = offset_y + (self.y + i) * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(surface, (0, 0, 0), rect)
