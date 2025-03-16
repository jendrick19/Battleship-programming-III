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
        gridSz (int): Tamaño de las cuadrículas (lado x lado).
        cellSz (int): Tamaño de cada celda de la cuadrícula en píxeles.
        offset_x (int): Desplazamiento horizontal para la cuadrícula de configuración.
        offset_y (int): Desplazamiento vertical para la cuadrícula de configuración.
        offset_x1 (int): Desplazamiento horizontal para la cuadrícula de posiciones del jugador durante el juego.
        offset_y1 (int): Desplazamiento vertical para la cuadrícula de posiciones del jugador durante el juego.
        offset_x2 (int): Desplazamiento horizontal para la cuadrícula de ataque durante el juego.
        offset_y2 (int): Desplazamiento vertical para la cuadrícula de ataque durante el juego.
        font (pygame.font.Font): Fuente utilizada para el texto.
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
    """
    def __init__(self, title, width, height):
        """
        Inicializa la superficie principal del juego.

        Args:
            title (str): Título de la ventana/superficie.
            width (int): Ancho de la superficie.
            height (int): Alto de la superficie.
        """
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

    def setup_player(self, name):
        """
        Crea el objeto Player para esta superficie y añade los barcos configurados a su flota.

        Args:
            name (str): El nombre del jugador.
        """
        self.player = Player(name)
        for ship in self.ships:
            ship.update_positions()  # Ensure positions are up to date
            game_ship = Ship(
                ship.length,
                ship.x,
                ship.y,
                ship.isHorizontal,
                f"Ship{ship.length}"
            )
            self.player.add_ship(game_ship)

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

    def draw(self):
        """
        Dibuja la superficie del juego, mostrando diferentes elementos según el estado actual.
        """
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

    def draw_setup(self):
        """
        Dibuja la interfaz de la fase de configuración, incluyendo la cuadrícula, los barcos arrastrables y el botón "Continue".
        """
        # Draw grid
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

        # Draw ships
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)

        # Draw buttons
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnContinue)

        textContinue = self.font.render('Continue', True, (255, 255, 255))


        rectContinue = textContinue.get_rect(center=self.btnContinue.center)

        self.surface.blit(textContinue, rectContinue)

        # Instructions
        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

    def draw_playing(self):
        """
        Dibuja la interfaz de la fase de juego, incluyendo las dos cuadrículas (posición propia y ataque del oponente),
        los disparos realizados y el botón "End Turn".
        """
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
        """
        Dibuja la pantalla de fin de juego, mostrando el ganador y el botón para reiniciar.
        """
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
        """
        Maneja los eventos de pygame, especialmente durante la fase de configuración para permitir el arrastre y rotación de los barcos.

        Args:
            events (list): Lista de eventos de pygame a procesar.
        """
        if self.state == "setup":
            for event in events:
                for ship in self.ships:
                    ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz)

    def handle_click(self, mouse_pos):
        """
        Maneja los clics del ratón, realizando acciones según el estado del juego y la posición del clic.

        Args:
            mouse_pos (tuple[int, int]): La posición (x, y) del clic del ratón.

        Returns:
            str or None: Una cadena que indica la acción realizada ("continue", "end_turn", "shot_made")
                         o None si no se realizó ninguna acción relevante.
        """
        if self.state == "setup":
            if self.btnContinue.collidepoint(mouse_pos):
                return "continue"
        else:  # playing state
            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.shot_made or self.game_over:
                    return "end_turn"
            else:
                return self.handle_attack(mouse_pos)
        return None

    def handle_attack(self, mouse_pos):
        """
        Maneja la lógica de un intento de ataque durante la fase de juego.

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
        self.shot_made = False
```

### ship.py

```
import pygame

class Ship:
    """
    Clase para representar un barco en el juego Battleship, con funcionalidades de colocación, rotación y seguimiento de daño.

    Atributos:
        length (int): Longitud del barco (número de celdas que ocupa).
        x (float): Posición horizontal del barco en la cuadrícula (en unidades de celda).
        y (float): Posición vertical del barco en la cuadrícula (en unidades de celda).
        life (int): Puntos de vida restantes del barco, inicialmente igual a su longitud.
        isHorizontal (bool): Indica si el barco está orientado horizontalmente (True) o verticalmente (False). Por defecto es True.
        name (str or None): Nombre del barco. Si es None, se genera automáticamente como "Ship{length}".
        position (list[tuple[int, int]]): Lista de coordenadas (fila, columna) que ocupa el barco en la cuadrícula. Se actualiza al mover o rotar el barco.

        # Atributos para la interfaz de usuario (UI)
        dragging (bool): Indica si el barco está siendo arrastrado por el jugador.
        offset_x (float): Desplazamiento horizontal interno durante el arrastre para mantener la posición relativa del ratón.
        offset_y (float): Desplazamiento vertical interno durante el arrastre para mantener la posición relativa del ratón.
    """
    def __init__(self, length, x, y, isHorizontal=True, name=None):
        """
        Inicializa un nuevo objeto Ship.

        Args:
            length (int): La longitud del barco.
            x (float): La posición inicial horizontal del barco en la cuadrícula.
            y (float): La posición inicial vertical del barco en la cuadrícula.
            isHorizontal (bool, optional): La orientación inicial del barco. Defaults to True (horizontal).
            name (str, optional): El nombre del barco. Defaults to None, en cuyo caso se genera un nombre automático.
        """
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
        """
        Calcula la lista de coordenadas (fila, columna) que ocupa el barco basado en su posición, longitud y orientación.

        Returns:
            list[tuple[int, int]]: Una lista de tuplas representando las celdas ocupadas por el barco.
        """
        positions = []
        if self.isHorizontal:
            for i in range(self.length):
                positions.append((int(self.y), int(self.x) + i))
        else:
            for i in range(self.length):
                positions.append((int(self.y) + i, int(self.x)))
        return positions

    def update_positions(self):
        """
        Actualiza el atributo `position` del barco llamando a `_calculate_positions()`.
        Debe llamarse después de cualquier cambio en `x`, `y` o `isHorizontal`.
        """
        self.position = self._calculate_positions()

    def check_sunken_ship(self):
        """
        Verifica si el barco ha sido hundido.

        Returns:
            bool: True si la vida del barco es 0, False en caso contrario.
        """
        return self.life == 0

    def damage_received_ship(self):
        """
        Reduce la vida del barco en 1 si aún tiene vida.
        """
        if self.life > 0:
            self.life -= 1

    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10):
        """
        Maneja los eventos de pygame para permitir arrastrar, soltar y rotar el barco en la cuadrícula durante la fase de configuración.

        Args:
            event (pygame.event.Event): El evento de pygame a procesar.
            offset_x (int): El desplazamiento horizontal de la cuadrícula en la pantalla.
            offset_y (int): El desplazamiento vertical de la cuadrícula en la pantalla.
            cellSize (int): El tamaño de cada celda de la cuadrícula en píxeles.
            gridSize (int, optional): El tamaño de la cuadrícula (lado x lado). Defaults to 10.
        """
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
        """
        Rota el barco 90 grados, ajustando su posición si es necesario para que permanezca dentro de los límites de la cuadrícula.

        Args:
            gridSize (int): El tamaño de la cuadrícula.
        """
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
        """
        Dibuja el barco en la superficie dada.

        Args:
            surface (pygame.Surface): La superficie en la que se va a dibujar el barco.
            offset_x (int): El desplazamiento horizontal de la cuadrícula en la pantalla.
            offset_y (int): El desplazamiento vertical de la cuadrícula en la pantalla.
            cellSize (int): El tamaño de cada celda de la cuadrícula en píxeles.
        """
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
```

### window.py

```
import pygame

class Window:
    """
    Clase para gestionar la ventana principal del juego.

    Atributos:
        width (int): Ancho de la ventana en píxeles.
        height (int): Alto de la ventana en píxeles.
        title (str): Título de la ventana.
        window (pygame.Surface): Objeto Surface que representa la ventana principal.
        font (pygame.font.Font): Fuente utilizada para el texto en la ventana.
        btnPlay (pygame.Rect): Rectángulo para el botón "Play" en el menú principal.
        btnExit (pygame.Rect): Rectángulo para el botón "Exit" en el menú principal.
    """
    def __init__(self, width, height, title):
        """
        Inicializa la ventana principal del juego.

        Args:
            width (int): Ancho deseado para la ventana.
            height (int): Alto deseado para la ventana.
            title (str): Título que se mostrará en la barra de la ventana.
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.window.fill((0, 128, 255))

        self.font = pygame.font.Font(None, 36) # Fuente predeterminada de Pygame, tamaño 36

        self.btnPlay = pygame.Rect(350, 250, 100, 50) # Rectángulo para el botón "Play"
        self.btnExit = pygame.Rect(350, 350, 100, 50) # Rectángulo para el botón "Exit"

    def drawBtns(self):
        """
        Dibuja los botones "Play" y "Exit" en el menú principal de la ventana.
        """
        self.window.fill((0, 128, 255))

        title = self.font.render(self.title, True, (255, 255, 255)) # Renderiza el título en blanco
        title_rect = title.get_rect(center=(self.width // 2, 100)) # Centra el título
        self.window.blit(title, title_rect) # Dibuja el título en la ventana

        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay) # Dibuja el botón "Play" en rojo
        pygame.draw.rect(self.window, (255, 0, 0), self.btnExit) # Dibuja el botón "Exit" en rojo

        play_text = self.font.render('Play', True, (255, 255, 255)) # Renderiza el texto "Play" en blanco
        exit_text = self.font.render('Exit', True, (255, 255, 255)) # Renderiza el texto "Exit" en blanco

        play_rect = play_text.get_rect(center=self.btnPlay.center) # Centra el texto en el botón "Play"
        exit_rect = exit_text.get_rect(center=self.btnExit.center) # Centra el texto en el botón "Exit"

        self.window.blit(play_text, play_rect) # Dibuja el texto "Play" en el botón
        self.window.blit(exit_text, exit_rect) # Dibuja el texto "Exit" en el botón

    def renderSurface(self, surface):
        """
        Dibuja una superficie dada sobre la ventana principal.

        Args:
            surface (pygame.Surface): La superficie a renderizar.
        """
        self.window.blit(surface, (0, 0))

    def updateWindow(self):
        """
        Actualiza toda la ventana para mostrar los cambios realizados.
        """
        pygame.display.update()
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
    y gestiona el flujo del juego entre la configuración y la partida.
    """
    pygame.init()

    window = Window(800, 600, 'BATTLESHIP')
    window.drawBtns()

    surfacePlayer1 = GameSurface('Choose the position of your ships player 1', 800, 600)
    surfacePlayer2 = GameSurface('Choose the position of your ships player 2', 800, 600)

    execute = True
    current_surface = None
    game_started = False

    while execute:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                execute = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos() #Obtención de la posición del mouse

                if current_surface is None:
                    # Menu principal
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
                        # Fin de la configuración de un jugador
                        if current_surface == surfacePlayer1:
                            surfacePlayer1.setup_player("Player 1")
                            current_surface = surfacePlayer2
                        elif current_surface == surfacePlayer2:
                            surfacePlayer2.setup_player("Player 2")

                            # Configurar oponentes
                            surfacePlayer1.setup_opponent(surfacePlayer2.player)
                            surfacePlayer2.setup_opponent(surfacePlayer1.player)

                            # Cambiar al modo de juego
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

            # Dibujar la superficie actual
            current_surface.handle_events(events)
            current_surface.draw()
            window.renderSurface(current_surface.surface)
        else:
            window.drawBtns() # Dibujar los botones del menú principal si no hay superficie activa

        window.updateWindow()

    pygame.quit()
    sys.exit()

# Iniciar el juego
game()
```
