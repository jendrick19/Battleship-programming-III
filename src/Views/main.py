import pygame
from src.Models.window import Window

pygame.init()
window = Window(800,600, 'BATTLESHIP')
window.drawBtns()

execute = True

while execute:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execute = False
    window.updateWindow()

