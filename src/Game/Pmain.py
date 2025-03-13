#Clase main de prueba borrar luego para elaboración de main real 

from board import Board
from ship import Ship
from player import Player
from game_logic import GameLogic
from turnmanager import TurnManager

# Inicialización del juego
player1 = Player("Jugador 1")
player2 = Player("Jugador 2")


turn_manager = TurnManager(player1, player2)

# Agregar barcos manualmente para prueba
player1.add_ship(Ship("Destructor", 3, "horizontal", [(2, 3), (2, 4), (2, 5)]))
player2.add_ship(Ship("Crucero", 2, "vertical", [(5, 5), (6, 5)]))

# Bucle del juego
while True:
    if turn_manager.play_turn():
        break
