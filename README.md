# Battleship-programming-III

Batalla Naval: Aprendiendo a programar juegos en equipo Este proyecto de Batalla Naval fue desarrollado como parte de la materia de Programación 3 en la Universidad Centroccidental Lisandro Alvarado

🛠️ Tecnologías

Python

🔧 Instalación y Configuración

Prerequisitos
Python ^3.13

🤝 Cómo Contribuir
Clona el proyecto

Crea una rama para tu feature (git checkout -b feat-amazing-feature)

Haz commit de tus cambios (git commit -m 'feat: amazing feature')

Haz Push a la rama (git push origin feat-amazing-feature)

Abre un Pull Request

Nota: antes de codificar una nueva funcionalidad ve a la sección de issues y PRs del repositorio y verifica que ya no se esté discutiendo sobre ese tema, o que ya otra persona no lo haya realizado.

📋 Estándares de Código

Commits

Si es posible describe tus proyectos para que los mantenedores los puedan analizar de una forma más rápida y eficiente.

feat: - Nuevas características

fix: - Correcciones de bugs

docs: - Cambios en documentación

style: - Cambios que afectan el estilo del código y/o diseño (espacios, formato, etc)

refact: - Refactorización del código

test: - Añadir o modificar tests

chore: - Cambios en el proceso de build o herramientas auxiliares

hotfix: - Correcciones de bugs críticos

Ejemplo: feat: add newsletter subscription component

Código

Utiliza en lo posible el estilo de codificación configurado

Nombra las variables y funciones en camelCase

Utiliza nombres descriptivos en variables y funciones

Comenta tu código cuando solo sea necesario

🚫 Qué evitar

No hagas commit directamente a main

No dejes print() en el código

No añadas dependencias sin discutirlo primero

No modifiques la configuración del proyecto sin consenso

Evita ser grosero o imponerte en las discusiones

## 📃 Documentación

### Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/jendrick19/Battleship-programming-III.git
   ```
2. Navega al directorio del proyecto:
   ```sh
   cd Battleship-programming-III
   ```
3. Instala las dependencias:
   ```sh
   pip install pygame
   ```

## 🚀 Ejecución del Proyecto

Para ejecutar el proyecto, simplemente corre el archivo main.py:

```sh
python src/Views/main.py
```

## 📁 Estructura del proyecto

```
.gitignore
README.md
src/
    Game/
        gameLogic.py
        player.py
    Models/
        board.py
        gameSurface.py
        ship.py
        window.py
    Views/
        main.py
```

### gameLogic.py

```
class GameLogic:
    """
    Clase que contiene la lógica principal del juego Battleship.

    Atributos:
        player1: El objeto que representa al jugador 1. Se espera que tenga un método `all_ships_sunken()` y un atributo `name`.
        player2: El objeto que representa al jugador 2. Se espera que tenga un método `all_ships_sunken()` y un atributo `name`.
    """
    def __init__(self, player1, player2):
        """
        Inicializa la lógica del juego con los dos jugadores.

        Args:
            player1: El objeto del primer jugador.
            player2: El objeto del segundo jugador.
        """
        self.player1 = player1
        self.player2 = player2

    def check_victory(self):
        """
        Verifica si alguno de los jugadores ha hundido todos los barcos del oponente.

        Returns:
            str or None: Retorna un mensaje indicando el nombre del ganador si hay uno,
                         o None si aún no hay ganador.
        """
        if self.player1.all_ships_sunken():
            return f"{self.player2.name} gano" # Jugador 2 gana si todos los barcos del jugador 1 están hundidos
        if self.player2.all_ships_sunken():
            return f"{self.player1.name} gano" # Jugador 1 gana si todos los barcos del jugador 2 están hundidos
        return None # No hay ganador aún
```

### player.py

```
from src.Models.board import Board
from src.Models.ship import Ship

class Player:
    """
    Clase para representar a un jugador en el juego Battleship.

    Atributos:
        name (str): El nombre del jugador.
        board (Board): El tablero de juego del jugador.
        ships (list[Ship]): La lista de barcos del jugador.
    """
    def __init__(self, name):
        """
        Inicializa un nuevo objeto Player.

        Args:
            name (str): El nombre del jugador.
        """
        self.name = name
        self.board = Board(10) # Crea un tablero de 10x10 para el jugador
        self.ships = []

    def add_ship(self, ship):
        """
        Añade un barco a la flota del jugador y actualiza la representación del tablero.

        Args:
            ship (Ship): El objeto Ship a añadir.
        """
        self.ships.append(ship)
        # Asume que el objeto Ship tiene un atributo 'position' que es una lista de tuplas (row, col)
        for row, col in ship.position:
            if 0 <= row < self.board.size and 0 <= col < self.board.size:
                self.board.grid[row][col] = 's' # Marca la posición del barco en el tablero con 's'

    def shoot_at_opponent(self, opponent, row, col):
        """
        Realiza un disparo contra el tablero de un oponente.

        Args:
            opponent (Player): El objeto Player del oponente.
            row (int): La fila del objetivo del disparo.
            col (int): La columna del objetivo del disparo.

        Returns:
            str: El resultado del disparo: "Disparo fallido" o "Disparo exitoso".
        """

        result = "Disparo fallido"

        if opponent.board.grid[row][col] == 's':
            opponent.board.grid[row][col] = 'x' # Marca el impacto en el tablero del oponente con 'x'
            result = "Disparo exitoso"

            # Asume que el objeto Ship tiene un atributo 'position' y un método 'damage_received_ship()'
            for ship in opponent.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship()
                    break
        else:
            opponent.board.grid[row][col] = 'o' # Marca el fallo en el tablero del oponente con 'o'

        return result

    def all_ships_sunken(self):
        """
        Verifica si todos los barcos del jugador han sido hundidos.
        """
        return all(ship.check_sunken_ship() for ship in self.ships)
```

### board.py

```
class Board:
    """
    Clase para representar el tablero de juego de Battleship.

    Atributos:
        size (int): La dimensión del tablero (lado x lado).
        grid (list[list[str]]): Una matriz 2D que representa el estado de cada celda del tablero.
                                 Cada celda puede contener:
                                 - 'w': Agua (sin barco ni disparo).
                                 - 's': Barco.
                                 - 'x': Impacto en un barco.
                                 - 'o': Disparo fallido en el agua.
    """
    def __init__(self, size):
        """
        Inicializa un nuevo tablero de juego.

        Args:
            size (int): La dimensión deseada para el tablero (por ejemplo, 10 para un tablero de 10x10).
        """
        self.size = size
        self.grid = [['w' for _ in range(self.size)] for _ in range(self.size)]
        # Inicializa la cuadrícula con 'w' (agua) en todas las celdas.
```

### gameSurface.py

```
import pygame
from src.Models.board import Board
from src.Game.player import Player
from src.Game.gameLogic import GameLogic
from src.Models.ship import Ship

class GameSurface:
    """
    Clase para gestionar la superficie principal del juego, controlando las fases de configuración y juego.

    Atributos:
        width (int): Ancho de la superficie en píxeles.
        height (int): Alto de la superficie en píxeles.
        title (str): Título de la superficie.
        surface (pygame.Surface): Objeto Surface principal del juego.
        colorT (tuple[int, int, int]): Color del texto del título.
        gridSz (int): Tamaño de las cuadrículas (lado x lado).
        cellSz (int): Tamaño de cada celda de la cuadrícula en píxeles.
        offset_x (int): Desplazamiento horizontal para la cuadrícula de configuración.
        offset_y (int): Desplazamiento vertical para la cuadrícula de configuración.
        backSur (pygame.image): Imagen de fondo de la superficie.
        font_tittle (pygame.font.Font): Fuente utilizada para el título.
        offset_x1 (int): Desplazamiento horizontal para la cuadrícula de posiciones del jugador durante el juego.
        offset_y1 (int): Desplazamiento vertical para la cuadrícula de posiciones del jugador durante el juego.
        offset_x2 (int): Desplazamiento horizontal para la cuadrícula de ataque durante el juego.
        offset_y2 (int): Desplazamiento vertical para la cuadrícula de ataque durante el juego.
        font (pygame.font.Font): Fuente utilizada para el texto general.
        state (str): Estado actual del juego ("setup" o "playing").
        player_number (int): Número del jugador (1 o 2), basado en el título.
        btnContinue (pygame.Rect): Rectángulo para el botón "Continue" durante la configuración.
        btnReset (pygame.Rect): Rectángulo para el botón "RESET GAME" al final del juego.
        btnEndTurn (pygame.Rect): Rectángulo para el botón "End Turn" durante el juego.
        ships (list[Ship]): Lista de objetos Ship disponibles para la configuración.
        player (Player): Objeto Player asociado a esta superficie.
        opponent (Player): Objeto Player del oponente.
        game_logic (GameLogic): Objeto GameLogic para gestionar las reglas del juego.
        hits (list[tuple[int, int]]): Lista de coordenadas (row, col) de los disparos exitosos.
        misses (list[tuple[int, int]]): Lista de coordenadas (row, col) de los disparos fallidos.
        shot_made (bool): Indica si el jugador actual ha realizado un disparo en su turno.
        game_over (bool): Indica si el juego ha terminado.
        winner (str or None): Nombre del jugador ganador o None si el juego no ha terminado.
        collision_message (str): Mensaje a mostrar en caso de colisión de barcos durante la configuración.
        message_timer (int): Tiempo en milisegundos hasta que desaparece el mensaje de colisión.
    """
    def __init__(self, title, width, height, colorT):
        """
        Inicializa la superficie principal del juego.

        Args:
            title (str): Título de la ventana/superficie.
            width (int): Ancho de la superficie.
            height (int): Alto de la superficie.
            colorT (tuple[int, int, int]): Color del texto del título.
        """
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
        """
        Crea el objeto Player para esta superficie y añade los barcos configurados a su flota,
        verificando previamente si hay colisiones entre los barcos.

        Args:
            name (str): El nombre del jugador.

        Returns:
            bool: True si el jugador se configuró correctamente (sin colisiones), False en caso contrario.
        """
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
        """
        Establece el objeto Player del oponente y la lógica del juego.

        Args:
            opponent (Player): El objeto Player del oponente.
        """
        self.opponent = opponent
        self.game_logic = GameLogic(self.player, self.opponent)

    def switch_to_playing(self):
        """
        Cambia el estado del juego a "playing".
        """
        self.state = "playing"

    def has_ship_collisions(self):
        """
        Verifica si hay colisiones entre los barcos en la fase de configuración.

        Returns:
            bool: True si hay al menos una colisión entre barcos, False en caso contrario.
        """
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i+1:]:
                if ship1.check_collision([ship2]):
                    return True
        return False

    def draw(self):
        """
        Dibuja la superficie del juego, mostrando diferentes elementos según el estado actual.
        """
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

    def draw_setup(self):
        """
        Dibuja la interfaz de la fase de configuración, incluyendo la cuadrícula, los barcos arrastrables y el botón "Continue".
        Muestra advertencias si hay colisiones entre los barcos.
        """
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
        """
        Dibuja la interfaz de la fase de juego, incluyendo las dos cuadrículas (posición propia y ataque del oponente),
        los disparos realizados y el botón "End Turn".
        """
        # Draw position grid
        titlePosit = self.font.render('POSITIONS', True, (255, 255, 255))
        self.surface.blit(titlePosit, (self.offset_x1 + 110, self.offset_y1 - 30))

        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (6, 190, 225), rect, 2)

                # Draw ships
                if self.player and (row, col) in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.rect(self.surface, (0, 0, 0), rect)

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
        """
        Dibuja la pantalla de fin de juego, mostrando el ganador y el botón para reiniciar.
        """
        self.title = "GAME OVER"

        textReset = self.font.render('RESET GAME', True, (255, 255, 255))
        rectReset = textReset.get_rect(center=self.btnReset.center)
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset)
        self.surface.blit(textReset, rectReset)

        game_over_text = self.font.render(f"{self.winner} WINS!", True, (255, 255, 0))
        message_win = game_over_text.get_rect(center=(self.width // 2, 300))
        self.surface.blit(game_over_text, message_win)

    def handle_events(self, events):
        """
        Maneja los eventos de pygame.

        Durante la fase de "setup", itera sobre los eventos y los pasa a cada barco
        para permitir la interacción del usuario (arrastrar y soltar).

        Args:
        events (list): Una lista de objetos pygame.event.Event a procesar.
        """
        if self.state == "setup":
            for event in events:
                for ship in self.ships:
                    ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz, self.ships)

    def handle_click(self, mouse_pos):
        """
        Maneja los clics del ratón en la superficie del juego.

        En la fase de "setup", verifica si se hizo clic en el botón "Continue".
        Si no hay colisiones entre los barcos, retorna "continue".
        Si hay colisiones, muestra un mensaje y establece un temporizador.

        En la fase de "playing", verifica si se hizo clic en el botón "End Turn".
        Si se ha realizado un disparo o el juego ha terminado, retorna "end_turn".
        Si no se hizo clic en el botón "End Turn", llama a `handle_attack`.

        Args:
            mouse_pos (tuple[int, int]): La posición (x, y) del clic del ratón.

        Returns:
            str or None: Una cadena que indica la acción ("continue", "end_turn", "shot_made")
                     o None si no se realizó ninguna acción relevante.
        """
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
        """
        Maneja los clics del ratón durante la fase de ataque ("playing").

        Verifica si el clic ocurrió dentro de la cuadrícula de ataque y si ya se
        realizó un disparo en este turno. No permite disparar en celdas ya atacadas.
        Utiliza el objeto `Player` para registrar el disparo en el oponente.
        Actualiza las listas de `hits` o `misses` según el resultado del disparo.
        Verifica si el juego ha terminado llamando a `game_logic.check_victory()`.
        Establece la bandera `shot_made` en True si se realizó un disparo.

        Args:
            mouse_pos (tuple[int, int]): La posición (x, y) del clic del ratón.

        Returns:
            str or None: "shot_made" si se realizó un disparo válido, None en caso contrario.
        """
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
        """
        Restablece la bandera `shot_made` a False, permitiendo al jugador realizar un nuevo disparo en su turno.
        """
        self.shot_made = False
```

### main.py

```
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pygame
from src.Models.window import Window
from src.Models.gameSurface import GameSurface

def game():
    """
    Función principal que ejecuta el juego Battleship.
    Inicializa Pygame, crea las ventanas y superficies necesarias,
    y gestiona el flujo del juego entre el menú, la configuración de los jugadores y la partida.
    """
    pygame.init()

    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    surfacePlayer1 = GameSurface('Choose the position of your ships player 1', 800, 600, (119, 255, 148))
    surfacePlayer2 = GameSurface('Choose the position of your ships player 2', 800, 600, (255, 163, 175))

    execute = True
    current_surface = None
    game_started = False

    while execute:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                execute = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos() # Obtiene la posición del ratón

                if current_surface is None:

                    if window.btnPlay.collidepoint(mouse_pos):
                        current_surface = surfacePlayer1
                        current_surface.draw()
                        window.renderSurface(current_surface.surface)

                    elif window.btnExit.collidepoint(mouse_pos):
                        execute = False

                else:
                    # Fases de configuración y juego
                    action = current_surface.handle_click(mouse_pos)

                    if action == "continue":
                        if current_surface == surfacePlayer1:
                            if current_surface.setup_player("Player 1"):
                                current_surface = surfacePlayer2
                        elif current_surface == surfacePlayer2:
                            if current_surface.setup_player("Player 2"):
                                # Set up opponents
                                surfacePlayer1.setup_opponent(surfacePlayer2.player)
                                surfacePlayer2.setup_opponent(surfacePlayer1.player)

                                # Switch to playing mode
                                surfacePlayer1.switch_to_playing()
                                surfacePlayer2.switch_to_playing()

                                current_surface = surfacePlayer1
                                game_started = True

                    elif action == "end_turn" and current_surface.game_over == False:
                        # Fin del turno de un jugador durante la partida
                        if current_surface == surfacePlayer1:
                            current_surface = surfacePlayer2
                            surfacePlayer2.reset_shot_flag()
                        else:
                            current_surface = surfacePlayer1
                            surfacePlayer1.reset_shot_flag()

        # Lógica para el botón de reinicio (si el juego ha terminado)
        if current_surface is not None:

            if current_surface.btnReset.collidepoint(mouse_pos) and current_surface.game_over:
                game() # Reiniciar el juego llamando a la función game() de nuevo
                return

            current_surface.handle_events(events)
            current_surface.draw()
            window.renderSurface(current_surface.surface)
        else:
            window.drawBtns() # Dibujar los botones del menú principal si no hay superficie activa

        window.updateWindow()

    pygame.quit()
    sys.exit()

game()
```
