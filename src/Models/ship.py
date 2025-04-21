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
        self.damage_positions = [False] * self.length

        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.is_colliding = False

        self.initial_x = x
        self.initial_y = y
        self.initial_isHorizontal = isHorizontal

    def _calculate_positions(self):
        return [(int(self.y) + i, int(self.x)) if not self.isHorizontal else (int(self.y), int(self.x) + i) for i in range(self.length)]

    def update_positions(self):
        self.position = self._calculate_positions()
        self.is_colliding = False

    def check_sunken_ship(self):
        return self.life == 0

    def damage_received_ship(self, x, y):
        for idx, pos in enumerate(self.position):
            if pos == (x, y):
                if not self.damage_positions[idx]:
                    self.damage_positions[idx] = True
                    self.life -= 1
                    return True
        return False

    def can_move(self, direction, board, other_ships):
        if self.check_sunken_ship():
            return False

        new_pos = []
        if direction == 'left' and self.isHorizontal:
            if self.damage_positions[0] or self.x - 1 < 0:
                return False
            new_pos = [(y, x - 1) for y, x in self.position]
        elif direction == 'right' and self.isHorizontal:
            if self.damage_positions[-1] or self.x + self.length >= board:
                return False
            new_pos = [(y, x + 1) for y, x in self.position]
        elif direction == 'up' and not self.isHorizontal:
            if self.damage_positions[0] or self.y - 1 < 0:
                return False
            new_pos = [(y - 1, x) for y, x in self.position]
        elif direction == 'down' and not self.isHorizontal:
            if self.damage_positions[-1] or self.y + self.length >= board:
                return False
            new_pos = [(y + 1, x) for y, x in self.position]
        else:
            return False

        for ship in other_ships:
            if ship == self:
                continue
            if set(new_pos) & set(ship.position):
                return False

        return True

    def move(self, direction):
        if direction == 'left': self.x -= 1
        elif direction == 'right': self.x += 1
        elif direction == 'up': self.y -= 1
        elif direction == 'down': self.y += 1
        self.update_positions()

    def check_collision(self, other_ships):
        my_positions = set(self.position)
        for ship in other_ships:
            if self == ship:
                continue
            if my_positions & set(ship.position):
                return True
        return False

    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10, other_ships=None):
        if other_ships is None:
            other_ships = []

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            rect = pygame.Rect(
                offset_x + self.x * cellSize,
                offset_y + self.y * cellSize,
                (self.length if self.isHorizontal else 1) * cellSize,
                (1 if self.isHorizontal else self.length) * cellSize
            )
            if rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                self.offset_x = self.x * cellSize - (mouse_x - offset_x)
                self.offset_y = self.y * cellSize - (mouse_y - offset_y)
                self.initial_x = self.x
                self.initial_y = self.y
                self.initial_isHorizontal = self.isHorizontal

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            self.x = int(self.x)
            self.y = int(self.y)
            self.update_positions()
            if other_ships and self.check_collision(other_ships):
                self.x = self.initial_x
                self.y = self.initial_y
                self.isHorizontal = self.initial_isHorizontal
                self.update_positions()
                self.is_colliding = True
            else:
                self.is_colliding = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.x = (mx - offset_x + self.offset_x) / cellSize
            self.y = (my - offset_y + self.offset_y) / cellSize
            if self.isHorizontal:
                self.x = max(0, min(gridSize - self.length, self.x))
                self.y = max(0, min(gridSize - 1, self.y))
            else:
                self.x = max(0, min(gridSize - 1, self.x))
                self.y = max(0, min(gridSize - self.length, self.y))
            self.update_positions()
            self.is_colliding = self.check_collision(other_ships)

        elif event.type == pygame.KEYDOWN and self.dragging and event.key == pygame.K_SPACE:
            self.rotate(gridSize)
            self.update_positions()
            self.is_colliding = self.check_collision(other_ships)

    def rotate(self, gridSize):
        if self.isHorizontal:
            center_x = self.x + self.length / 2
            center_y = self.y + 0.5
        else:
            center_x = self.x + 0.5
            center_y = self.y + self.length / 2

        self.isHorizontal = not self.isHorizontal

        if self.isHorizontal:
            self.x = max(0, min(gridSize - self.length, center_x - self.length / 2))
            self.y = max(0, min(gridSize - 1, center_y - 0.5))
        else:
            self.x = max(0, min(gridSize - 1, center_x - 0.5))
            self.y = max(0, min(gridSize - self.length, center_y - self.length / 2))
        self.update_positions()

    def draw(self, surface, offset_x, offset_y, cellSize):
        base_color = (50, 50, 50)
        if self.is_colliding:
            base_color = (255, 0, 0)

        for i in range(self.length):
            x = offset_x + (self.x + i) * cellSize if self.isHorizontal else offset_x + self.x * cellSize
            y = offset_y + self.y * cellSize if self.isHorizontal else offset_y + (self.y + i) * cellSize
            rect = pygame.Rect(x, y, cellSize, cellSize)
            color = (255, 0, 0) if self.damage_positions[i] else base_color
            pygame.draw.rect(surface, color, rect)
