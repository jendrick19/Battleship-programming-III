import pygame

class Ship:
    def __init__(self, length, x, y):
        self.length = length
        self.x = x
        self.y = y
        self.hits = 0
        self.sunk = False
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event, offset_x, offset_y, cell_size):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                ship_rect = pygame.Rect(
                    offset_x + self.x * cell_size,
                    offset_y + self.y * cell_size,
                    self.length * cell_size,
                    cell_size
                )
                if ship_rect.collidepoint(mouse_x, mouse_y):
                    self.dragging = True
                    self.offset_x = self.x * cell_size - (mouse_x - offset_x)
                    self.offset_y = self.y * cell_size - (mouse_y - offset_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
                self.x = round((self.x * cell_size) / cell_size)
                self.y = round((self.y * cell_size) / cell_size)

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.x = (mouse_x - offset_x + self.offset_x) / cell_size
                self.y = (mouse_y - offset_y + self.offset_y) / cell_size

    def draw(self, surface, offset_x, offset_y, cell_size):
        for i in range(self.length):
            x = offset_x + (self.x + i) * cell_size
            y = offset_y + self.y * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, (0, 0, 0), rect)