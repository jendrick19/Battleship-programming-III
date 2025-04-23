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
    Link/
        client.py
        connection.py
        server.py
    Models/
        board.py
        gameSurface.py
        ship.py
        window.py
    Views/
        main.py
```

## Game

### gameLogic.py

**Rol**: Maneja la lógica básica del juego, especialmente la verificación de victoria.

**Clase principal:**

- `GameLogic`: Contiene la lógica principal del juego.

**Métodos principales:**

- `check_victory`: Verifica si algún jugador ha ganado.

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

**Rol**: Representa a un jugador, sus barcos y su tablero.

**Clase principal:**

- `Player`: Representa a un jugador del juego.

**Métodos principales:**

- `add_ship`: Añade un barco al tablero del jugador.
- `shoot_at_opponent`: Realiza un disparo al oponente.
- `all_ships_sunken`: Verifica si todos los barcos del jugador están hundidos.

**Variables importantes:**

- `board`: Instancia de Board que representa el tablero del jugador.
- `ships`: Lista de barcos del jugador.
- `hits`, `misses`: Registro de disparos acertados y fallidos.
- `damaged_positions`: Posiciones de barcos que han sido dañadas.

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
        self.damaged_positions = set()  # Conjunto para rastrear posiciones dañadas
        self.hits = []  # Posiciones donde el jugador ha acertado
        self.misses = []  # Posiciones donde el jugador ha fallado

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

            # Registrar el acierto
            self.hits.append((row, col))

            # Asume que el objeto Ship tiene un atributo 'position' y un método 'damage_received_ship()'
            for ship in opponent.ships:
                if (row, col) in ship.position:
                    ship.damage_received_ship()
                    # Añadir a las posiciones dañadas
                    opponent.damaged_positions.add((row, col))
                    break
        else:
            opponent.board.grid[row][col] = 'o' # Marca el fallo en el tablero del oponente con 'o'
            # Registrar el fallo
            self.misses.append((row, col))

        return result

    def all_ships_sunken(self):
        """
        Verifica si todos los barcos del jugador han sido hundidos.
        """
        return all(ship.check_sunken_ship() for ship in self.ships)
```

## Link

**Rol**: Los archivos client.py y server.py Implementan el cliente y servidor para el modo multijugador.

**Funcionalidad principal:**

- Establecen conexión usando la clase Conexion.
- Implementan un chat básico como prueba de concepto.

### client.py

```
from connection import Conexion

def main():
    """
    Función principal que ejecuta el cliente para conectarse al servidor.

    - Inicializa la conexión con el servidor especificando el modo cliente (`modo_servidor=False`), la dirección IP del servidor y el puerto.
    - Entra en un bucle infinito para enviar mensajes al servidor y recibir sus respuestas.
    - Solicita al usuario que escriba un mensaje para enviar.
    - Envía el mensaje al servidor utilizando el método `enviar_datos` de la conexión.
    - Recibe la respuesta del servidor utilizando el método `recibir_datos` de la conexión.
    - Imprime el mensaje recibido del servidor en la consola.
    """
    # Cambiar modo_servidor a False, ya que el cliente se conecta al servidor
    red = Conexion(modo_servidor=False, ip="192.168.0.5", puerto=5000)  # Cambia esta IP a la del servidor

    while True:
        # Enviar un mensaje al servidor
        mensaje = input("Escribe un mensaje: ")
        red.enviar_datos({"mensaje": mensaje})

        # Recibir respuesta del servidor
        respuesta = red.recibir_datos()
        print("Servidor dice:", respuesta["mensaje"])

main()
```

### connection.py

**Rol**: Maneja la conexión de red entre cliente y servidor.

**Clase principal:**

- `Conexion`: Maneja la comunicación de red.

**Métodos principales:**

1. **`__init__(self, modo_servidor: bool, ip: str = "0.0.0.0", puerto: int = 5000)`**

   - Constructor que inicializa la conexión.
   - **Parámetros**:
     - `modo_servidor`: True para servidor, False para cliente
     - `ip`: Dirección IP
     - `puerto`: Puerto de conexión

2. **`_iniciar_como_servidor(self)`**

   - Configura la conexión como servidor.

3. **`_iniciar_como_cliente(self)`**

   - Configura la conexión como cliente.

4. **`enviar_datos(self, info: dict)`**

   - Envía datos a través de la conexión.
   - **Parámetros**:
     - `info`: Diccionario con datos a enviar

5. **`recibir_datos(self) -> dict`**

   - Recibe datos de la conexión.
   - **Retorna**: Diccionario con datos recibidos

6. **`finalizar(self)`**
   - Cierra la conexión.

**Variables**

- `modo_servidor`: Indica si es servidor o cliente
- `ip`, `puerto`: Configuración de red
- `sock`: Socket de conexión
- `canal`: Canal de comunicación

```
import socket
import json

class Conexion:
    """
    Clase para manejar la conexión de red, tanto para el servidor como para el cliente.

    Atributos:
        modo_servidor (bool): Indica si la instancia actuará como servidor (True) o cliente (False).
        ip (str): La dirección IP a la que se enlazará (servidor) o a la que se conectará (cliente). Por defecto es "0.0.0.0".
        puerto (int): El puerto a utilizar para la conexión. Por defecto es 5000.
        sock (socket.socket): El objeto socket subyacente.
        canal (socket.socket o None): El canal de comunicación (socket conectado) para el servidor o el cliente. Es None hasta que se establece la conexión.
    """
    def __init__(self, modo_servidor: bool, ip: str = "0.0.0.0", puerto: int = 5000):
        """
        Inicializa una nueva instancia de la clase Conexion.

        Args:
            modo_servidor (bool): True si se inicia como servidor, False como cliente.
            ip (str, optional): La dirección IP para el enlace o la conexión. Por defecto es "0.0.0.0".
            puerto (int, optional): El puerto para la conexión. Por defecto es 5000.
        """
        self.modo_servidor = modo_servidor
        self.ip = ip
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.canal = None

        if self.modo_servidor:
            self._iniciar_como_servidor()
        else:
            self._iniciar_como_cliente()

    def _iniciar_como_servidor(self):
        """
        Inicia el socket y espera una conexión entrante como servidor.
        """
        try:
            self.sock.bind((self.ip, self.puerto))
            self.sock.listen(1)
            print(f"[SERVIDOR] Esperando conexión en {self.ip}:{self.puerto}...")
            self.canal, direccion = self.sock.accept()
            print(f"[SERVIDOR] Cliente conectado desde {direccion}")
        except Exception as error:
            raise ConnectionError(
                f"[ERROR SERVIDOR] No se pudo iniciar el servidor: {error}"
            )

    def _iniciar_como_cliente(self):
        """
        Intenta conectar el socket al servidor especificado como cliente.
        """
        try:
            self.sock.connect((self.ip, self.puerto))
            self.canal = self.sock
            print(f"[CLIENTE] Conectado al servidor en {self.ip}:{self.puerto}")
        except Exception as error:
            raise ConnectionError(
                f"[ERROR CLIENTE] No se pudo conectar al servidor: {error}"
            )

    def enviar_datos(self, info: dict):
        """
        Envía un diccionario de datos codificado en JSON a través del canal de conexión.

        Args:
            info (dict): El diccionario de datos a enviar.
        """
        try:
            mensaje = json.dumps(info).encode("utf-8")
            self.canal.sendall(mensaje)
        except Exception as error:
            print(f"[ERROR ENVÍO] {error}")

    def recibir_datos(self) -> dict:
        """
        Recibe datos a través del canal de conexión y los decodifica de JSON a un diccionario.

        Returns:
            dict: El diccionario de datos recibido. Retorna un diccionario vacío en caso de error.
        """
        try:
            datos = self.canal.recv(1024).decode("utf-8")
            return json.loads(datos)
        except Exception as error:
            print(f"[ERROR RECEPCIÓN] {error}")
            return {}

    def finalizar(self):
        """
        Cierra el canal de conexión y el socket principal.
        """
        try:
            if self.canal:
                self.canal.close()
            self.sock.close()
            print("[CONEXIÓN] Cerrada exitosamente")
        except Exception as error:
            print(f"[ERROR AL CERRAR] {error}")
```

### server.py

```
from connection import Conexion

def main():
    """
    Función principal que ejecuta el servidor para escuchar y comunicarse con los clientes.

    - Inicializa la conexión en modo servidor (`modo_servidor=True`) con la dirección IP y el puerto especificados.
    - Entra en un bucle infinito para escuchar las comunicaciones de los clientes.
    - Recibe datos del cliente utilizando el método `recibir_datos` de la conexión.
    - Imprime el mensaje recibido del cliente en la consola.
    - Solicita al servidor que escriba un mensaje para enviar al cliente.
    - Envía la respuesta al cliente utilizando el método `enviar_datos` de la conexión.
    """
    # Cambiar modo_servidor a True, ya que el servidor espera conexiones
    red = Conexion(modo_servidor=True, ip="192.168.0.5", puerto=5000)  # Cambia esta IP a la del servidor

    while True:
        # Recibimos los datos del cliente
        datos = red.recibir_datos()
        print("Cliente dice:", datos["mensaje"])

        # Enviar una respuesta al cliente
        mensaje = input("Escribe un mensaje para enviar al cliente: ")
        red.enviar_datos({"mensaje": mensaje})

main()
```

## Models

### board.py

**Rol**: Representa el tablero de juego.

**Clase principal:**

- `Board`: Representa un tablero de juego.

**Variables importantes:**

- `grid`: Matriz que representa el estado de cada celda ('w' para agua, 's' para barco, etc.).

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

**Responsabilidad**: Manejar la interfaz gráfica del juego.

**Clase principal:**

- `GameSurface`: Representa la superficie de juego para un jugador.

**Métodos principales:**

1. **`__init__(self, title, width, height, colorT)`**

   - Constructor que inicializa la superficie del juego.
   - **Parámetros**:
     - `title`: Título de la ventana
     - `width`: Ancho
     - `height`: Alto
     - `colorT`: Color del título

2. **`setup_player(self, name)`**

   - Configura un jugador con su nombre y barcos.
   - **Parámetros**:
     - `name`: Nombre del jugador
   - **Retorna**: True si la configuración fue exitosa

3. **`setup_opponent(self, opponent)`**

   - Configura el oponente del jugador.
   - **Parámetros**:
     - `opponent`: Jugador oponente

4. **`switch_to_playing(self)`**

   - Cambia el estado del juego a "jugando".

5. **`has_ship_collisions(self)`**

   - Verifica si hay colisiones entre barcos.
   - **Retorna**: True si hay colisiones

6. **`draw(self)`**

   - Dibuja toda la interfaz del juego según el estado actual.

7. **`handle_events(self, events)`**

   - Maneja eventos de entrada.
   - **Parámetros**:
     - `events`: Lista de eventos de pygame

8. **`handle_click(self, mouse_pos)`**

   - Maneja clics del mouse.
   - **Parámetros**:
     - `mouse_pos`: Posición del mouse
   - **Retorna**: Acción realizada

9. **`handle_ship_selection(self, row, col)`**

   - Maneja la selección de un barco.
   - **Parámetros**:
     - `row`: Fila seleccionada
     - `col`: Columna seleccionada
   - **Retorna**: "ship_selected" si se seleccionó un barco

10. **`move_selected_ship(self, direction)`**

    - Mueve el barco seleccionado.
    - **Parámetros**:
      - `direction`: Dirección del movimiento
    - **Retorna**: "ship_moved" si se movió el barco

11. **`handle_attack(self, mouse_pos, row, col)`**

    - Maneja un ataque a una posición.
    - **Parámetros**:
      - `mouse_pos`: Posición del mouse
      - `row`: Fila del ataque
      - `col`: Columna del ataque
    - **Retorna**: "shot_made" si se realizó un disparo

12. **`reset_shot_flag(self)`**
    - Reinicia las banderas de acción y disparo.

**Variables Principales**

- Variables de interfaz: `width`, `height`, `title`, `surface`, `colorT`, `gridSz`, `cellSz`, etc.
- Variables de estado: `state`, `player_number`, `action_taken`, `game_over`, `winner`
- Elementos de juego: `player`, `opponent`, `game_logic`, `ships`
- Elementos UI: `btnContinue`, `btnReset`, `btnEndTurn`, `btnConfirmYes`, `btnConfirmNo`, etc.
- Listas de seguimiento: `hits`, `misses`, `damaged_positions`

**Variables importantes:**

- `state`: Indica si está en fase de configuración ("setup") o juego ("playing").
- `player`, `opponent`: Instancias de Player para el jugador actual y su oponente.
- `game_logic`: Instancia de GameLogic para manejar la lógica del juego.
- `selected_ship`: Barco actualmente seleccionado para mover.
- `action_taken`: Indica si el jugador ya realizó una acción en su turno.
- `hits`, `misses`: Registro de disparos acertados y fallidos.

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
        title (str): Título de la superficie que se mostrará.
        surface (pygame.Surface): Objeto Surface principal para dibujar.
        colorT (tuple[int, int, int]): Color del texto del título.
        gridSz (int): Tamaño del lado de la cuadrícula del tablero (por defecto 10x10).
        cellSz (int): Tamaño de cada celda de la cuadrícula en píxeles.
        offset_x (int): Desplazamiento horizontal de la cuadrícula de colocación.
        offset_y (int): Desplazamiento vertical de la cuadrícula de colocación.
        backSur (pygame.image): Imagen de fondo de la superficie.
        font_tittle (pygame.font.Font): Fuente utilizada para el título.
        show_confirmation (bool): Indica si se debe mostrar el diálogo de confirmación de la colocación.
        option_allow_reshoot (bool): Indica si se permite disparar a celdas vacías ya atacadas.

        # Atributos para la fase de juego
        offset_x1 (int): Desplazamiento horizontal de la cuadrícula de posiciones del jugador.
        offset_y1 (int): Desplazamiento vertical de la cuadrícula de posiciones del jugador.
        offset_x2 (int): Desplazamiento horizontal de la cuadrícula de ataque del oponente.
        offset_y2 (int): Desplazamiento vertical de la cuadrícula de ataque del oponente.
        font (pygame.font.Font): Fuente utilizada para el texto en la fase de juego.
        state (str): Estado actual de la superficie ("setup" o "playing").
        player_number (int): Número del jugador (1 o 2).

        # Botones
        btnContinue (pygame.Rect): Rectángulo del botón "Continue" durante la colocación.
        btnReset (pygame.Rect): Rectángulo del botón "Reset Game" al finalizar la partida.
        btnEndTurn (pygame.Rect): Rectángulo del botón "End Turn" durante la partida.
        btnConfirmYes (pygame.Rect): Rectángulo del botón "Sí" en el diálogo de confirmación.
        btnConfirmNo (pygame.Rect): Rectángulo del botón "No" en el diálogo de confirmación.
        btnMoveUp (pygame.Rect): Rectángulo del botón para mover el barco seleccionado hacia arriba.
        btnMoveDown (pygame.Rect): Rectángulo del botón para mover el barco seleccionado hacia abajo.
        btnMoveLeft (pygame.Rect): Rectángulo del botón para mover el barco seleccionado hacia la izquierda.
        btnMoveRight (pygame.Rect): Rectángulo del botón para mover el barco seleccionado hacia la derecha.
        btncoords (pygame.Rect): Rectángulo del botón/input para ingresar coordenadas de ataque.
        active (bool): Indica si el input de coordenadas está activo.
        input_text (str): Texto ingresado en el input de coordenadas.
        colorI (tuple[int, int, int]): Color inactivo del botón de coordenadas.
        colorA (tuple[int, int, int]): Color activo del botón de coordenadas.
        error_message (str): Mensaje de error para la entrada de coordenadas.

        # Estado de selección de barco
        selected_ship (Ship or None): El barco actualmente seleccionado por el jugador.
        ship_selection_active (bool): Indica si la selección de barcos está activa.

        # Control de acciones por turno
        action_taken (bool): Indica si el jugador ya realizó una acción (mover o disparar) en su turno.

        # Rastreo de posiciones dañadas
        damaged_positions (set[tuple[int, int]]): Conjunto de posiciones (fila, columna) donde se ha dañado un barco.

        # Barcos para la fase de colocación
        ships (list[Ship]): Lista de objetos Ship que el jugador debe colocar.

        # Objetos del juego
        player (Player or None): Objeto Player asociado a esta superficie.
        opponent (Player or None): Objeto Player del oponente.
        game_logic (GameLogic or None): Objeto GameLogic para verificar las condiciones del juego.

        # Rastreo de UI durante la partida
        hits (list[tuple[int, int]]): Lista de coordenadas (fila, columna) donde el jugador ha acertado.
        misses (list[tuple[int, int]]): Lista de coordenadas (fila, columna) donde el jugador ha fallado.
        shot_made (bool): Indica si el jugador ha realizado un disparo en su turno.
        game_over (bool): Indica si la partida ha terminado.
        winner (str or None): Nombre del jugador ganador.

        collision_message (str): Mensaje de colisión de barcos durante la colocación.
        message_timer (int): Tiempo en milisegundos hasta que desaparece el mensaje.
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
        self.show_confirmation = False
        self.option_allow_reshoot = True

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
        self.btnConfirmYes = pygame.Rect(300 ,300, 80, 40)
        self.btnConfirmNo = pygame.Rect(410, 300, 80, 40)

        # Botones para mover barcos
        self.btnMoveUp = pygame.Rect(100, 450, 40, 40)
        self.btnMoveDown = pygame.Rect(100, 550, 40, 40)
        self.btnMoveLeft = pygame.Rect(60, 500, 40, 40)
        self.btnMoveRight = pygame.Rect(140, 500, 40, 40)

        # Boton para disparar
        self.btncoords = pygame.Rect(580, 450, 160, 40)
        self.active = False

        self.input_text = ""
        self.colorI = (0,0,0)
        self.colorA = (0, 255, 0)

        self.error_message = ""

        # Estado para selección de barco
        self.selected_ship = None
        self.ship_selection_active = False

        # Control de acciones por turno
        self.action_taken = False  # Indica si ya se realizó una acción (mover o disparar)

        # Rastreo de posiciones dañadas en el tablero
        self.damaged_positions = set()  # Conjunto de posiciones (row, col) donde se ha dañado un barco

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
        Crea el objeto Player para esta superficie y asigna los barcos colocados.

        Verifica si hay colisiones entre los barcos antes de crear el jugador.

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
        Establece el objeto Player del oponente y el objeto GameLogic.

        Args:
            opponent (Player): El objeto Player del oponente.
        """
        self.opponent = opponent
        self.game_logic = GameLogic(self.player, self.opponent)

    def switch_to_playing(self):
        """
        Cambia el estado de la superficie a "playing".
        """
        self.state = "playing"

    def has_ship_collisions(self):
        """
        Verifica si hay colisiones entre los barcos en la fase de colocación.

        Returns:
            bool: True si hay al menos una colisión, False en caso contrario.
        """
        for i, ship1 in enumerate(self.ships):
            for ship2 in self.ships[i+1:]:
                if ship1.check_collision([ship2]):
                    return True
        return False

    def draw(self):
        """
        Dibuja la superficie del juego, incluyendo el fondo, título y el estado actual
        (colocación, juego o fin de partida). También muestra mensajes de colisión.
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
            self.surface.blit(message, (self.width // 2 - message.get_width() // 2, 475))

    def draw_coordinates_button(self):
        """
        Dibuja el botón y las instrucciones para ingresar las coordenadas de ataque.
        """
        # dibujar formato de las coordenadas
        format_text = self.font.render("Format: A1 or B5", True, (255, 255, 255))
        self.surface.blit(format_text, (self.btncoords.x + 5, self.btncoords.y - 20))
        # dibujar el limite de las coordenadas
        limit_text = self.font.render("Limit: A1 to J10", True, (255, 255, 255))
        self.surface.blit(limit_text, (self.btncoords.x + 5, self.btncoords.y + 50))

        self.color = self.colorA if self.active else self.colorI # Cambiado a verde si el botón está activo

        # Dibuja el botón de las coordenadas
        pygame.draw.rect(self.surface, self.color, self.btncoords, 2)
        button_text = self.input_text if self.active else "Enter coordinates"
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.btncoords.center)
        self.surface.blit(text_surface, text_rect)

    def handle_attack_input(self, input_text):
        """
        Maneja la entrada de texto para las coordenadas de ataque.

        Valida el formato de la entrada y la convierte a coordenadas de la cuadrícula.
        Si la entrada es válida, llama a `handle_attack`.

        Args:
            input_text (str): El texto ingresado por el jugador.

        Returns:
            str or None: Un mensaje de error si la entrada no es válida, None en caso contrario.
        """
        self.error_message = ""
        # Validate the input (e.g., "A1", "B5")
        if len(input_text) < 2 or not input_text[0].isalpha() or not input_text[1:].isdigit():
            self.error_message = "Invalid coordinate format!"
            self.active = False
            return self.error_message

        # Convert the input to grid coordinates
        row = ord(input_text[0].upper()) - ord('A')  # Convert letter to row index
        col = int(input_text[1:]) - 1  # Convert number to column index

        # Check if the coordinates are within the grid
        if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
            self.handle_attack(None, row, col)  # Call the existing attack logic
            self.action_taken = True
            self.active = False
        else:
            self.error_message = "Coordinates out of bounds!"
            self.active = False
            return self.error_message


    def draw_confirmation_dialog(self):
        """
        Dibuja el diálogo de confirmación para la colocación de los barcos.
        """
       # Fondo del cuadroscreen
        pygame.draw.rect(self.surface, (0, 0, 0), (200, 200, 400, 200))
        pygame.draw.rect(self.surface, (255, 255, 255), (200, 200, 400, 200), 2)

        # Texto
        text = self.font.render("¿Estás seguro de tus posiciones?", True, (255, 255, 255))
        self.surface.blit(text, (self.width // 2 - text.get_width() // 2, 230))

        # Botones
        pygame.draw.rect(self.surface, (0, 200, 0), self.btnConfirmYes)
        pygame.draw.rect(self.surface, (200, 0, 0), self.btnConfirmNo)

        yes_text = self.font.render("Sí", True, (255, 255, 255))
        no_text = self.font.render("No", True, (255, 255, 255))

        self.surface.blit(yes_text, self.btnConfirmYes.move(30, 12))
        self.surface.blit(no_text, self.btnConfirmNo.move(30, 12))

    def draw_setup(self):
        """
        Dibuja la interfaz de la fase de colocación de barcos.

        Esto incluye:
        - La cuadrícula donde el jugador coloca sus barcos.
        - Los barcos que el jugador debe colocar, mostrando su posición actual.
        - El botón "Continue" para pasar a la siguiente fase una vez que los barcos están colocados.
        - Instrucciones sobre cómo rotar los barcos.
        - Un mensaje de advertencia si hay colisiones entre los barcos.
        - El diálogo de confirmación si el jugador ha presionado "Continue".
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
        button_color = (100, 100, 100) if has_collisions else (0, 200, 0) # Cambiado a verde si no hay colisiones
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

        if self.show_confirmation:
            self.draw_confirmation_dialog()

    def draw_playing(self):
        """
        Dibuja la interfaz de la fase de juego.

        Esto incluye:
        - La cuadrícula de "POSITIONS" del jugador, mostrando sus barcos y los disparos recibidos.
        - La cuadrícula de "ATTACK" del jugador, mostrando los disparos realizados al oponente.
        - Marcas visuales para impactos (rojas) y fallos (blancas) en la cuadrícula de ataque.
        - Representación visual de los barcos del jugador, indicando las partes dañadas.
        - El botón "End Turn" para finalizar el turno del jugador.
        - Un botón/input para ingresar las coordenadas de ataque.
        - Botones para mover el barco seleccionado si no se ha realizado una acción.
        - Información sobre la cantidad de barcos hundidos del oponente.
        - Mensajes de estado del turno (por ejemplo, "Disparo realizado", "Barco movido").
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

                # Dibujar posiciones dañadas (donde había un barco pero se movió)
                if (row, col) in self.damaged_positions and (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                    pygame.draw.circle(self.surface, (150, 150, 150),
                                      (x + self.cellSz // 2, y + self.cellSz // 2),
                                      self.cellSz // 3,
                                      3)

        # Dibujar barcos
        for ship in self.player.ships:
            is_selected = (ship == self.selected_ship)

            # Dibujar cada segmento del barco
            for i, pos in enumerate(ship.position):
                row, col = pos
                x = self.offset_x1 + col * self.cellSz
                y = self.offset_y1 + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)

                # Color según estado: dañado, seleccionado o normal
                if ship.damage_positions[i]:
                    color = (255, 0, 0)  # Rojo para partes dañadas
                elif is_selected:
                    color = (0, 255, 0)  # Verde para barco seleccionado
                else:
                    color = (0, 0, 0)    # Negro para barcos normales

                pygame.draw.rect(self.surface, color, rect)

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
        button_color = (255, 0, 0) if self.action_taken else (100, 100, 100)
        pygame.draw.rect(self.surface, button_color, self.btnEndTurn)

        textEndTurn = self.font.render('End Turn', True, (255, 255, 255))
        rectEndTurn = textEndTurn.get_rect(center=self.btnEndTurn.center)
        self.surface.blit(textEndTurn, rectEndTurn)

        # Dibujar botón de coordenadas
        self.draw_coordinates_button()

        # Dibujar botones de movimiento si hay un barco seleccionado y no se ha realizado una acción
        if self.selected_ship and not self.action_taken:
            # Botón arriba
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveUp)
            pygame.draw.polygon(self.surface, (255, 255, 255),
                               [(100 + 20, 450 + 10), (100 + 10, 450 + 30), (100 + 30, 450 + 30)])

            # Botón abajo
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveDown)
            pygame.draw.polygon(self.surface, (255, 255, 255),
                               [(100 + 20, 550 + 30), (100 + 10, 550 + 10), (100 + 30, 550 + 10)])

            # Botón izquierda
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveLeft)
            pygame.draw.polygon(self.surface, (255, 255, 255),
                               [(60 + 10, 500 + 20), (60 + 30, 500 + 10), (60 + 30, 500 + 30)])

            # Botón derecha
            pygame.draw.rect(self.surface, (0, 150, 255), self.btnMoveRight)
            pygame.draw.polygon(self.surface, (255, 255, 255),
                               [(140 + 30, 500 + 20), (140 + 10, 500 + 10), (140 + 10, 500 + 30)])

            # Instrucciones para mover barcos
            move_text = self.font.render("Move your selected ship", True, (255, 255, 255))
            self.surface.blit(move_text, (10, 430))

        # Display game status
        if self.player and self.opponent:
            ships_sunk = sum(1 for ship in self.opponent.ships if ship.check_sunken_ship())
            total_ships = len(self.opponent.ships)
            status_text = self.font.render(f"Ships sunk: {ships_sunk}/{total_ships}", True, (255, 255, 255))
            self.surface.blit(status_text, (600, 545))

            # Display turn status
            if self.action_taken:
                if self.shot_made:
                    turn_status = self.font.render("Shot made! Click End Turn", True, (255, 255, 0))
                else:
                    turn_status = self.font.render("Ship moved! Click End Turn", True, (255, 255, 0))
                self.surface.blit(turn_status, (300, 450))

            elif not self.action_taken and self.error_message == "Invalid coordinate format!":
                turn_status = self.font.render("Invalid coordinate format!", True, (255, 0, 0))
                self.surface.blit(turn_status, (300, 450))

            elif not self.action_taken and self.error_message == "Coordinates out of bounds!":
                turn_status = self.font.render("Coordinates out of bounds!", True, (255, 0, 0))
                self.surface.blit(turn_status, (300, 450))


            else:
                turn_status = self.font.render("Move a ship or Make a shot", True, (255, 255, 255))
                self.surface.blit(turn_status, (300, 450))

    def draw_game_over(self):
        """
        Dibuja la pantalla de fin de partida.

        Esto incluye:
        - Cambiar el título de la superficie a "GAME OVER".
        - Dibujar un botón de "RESET GAME" para permitir al jugador iniciar una nueva partida.
        - Mostrar un mensaje indicando el ganador de la partida.
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
        Maneja los eventos de Pygame específicos para la superficie actual.

        En la fase de "setup":
        - Permite que cada barco maneje sus propios eventos.

        En la fase de "playing":
        - Detecta clics en el botón de coordenadas para activar la entrada de texto.
        - Captura la entrada de texto del teclado cuando la entrada de coordenadas está activa.
        - Maneja la tecla "ENTER" para procesar la entrada de coordenadas como un ataque.
        - Maneja la tecla "BACKSPACE" para borrar caracteres de la entrada de coordenadas.
        """
        if self.state == "setup":
            for event in events:
                for ship in self.ships:
                    ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz, self.ships)
        if self.state == "playing":
            for event in events:
                mouse_pos = pygame.mouse.get_pos()
                if not self.action_taken:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btncoords.collidepoint(mouse_pos):
                            self.active = True
                        else:
                            self.active = False
                    if event.type == pygame.KEYDOWN and self.active:
                        if event.key == pygame.K_RETURN:
                            self.handle_attack_input(self.input_text)
                            self.input_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode
    def handle_click(self, mouse_pos):
        """
        Maneja los eventos de clic del ratón en diferentes elementos de la superficie.

        En el diálogo de confirmación (durante la fase de "setup"):
        - Detecta clics en los botones "Sí" y "No" y actualiza el estado de confirmación.

        En la fase de "setup":
        - Detecta clics en el botón "Continue" y muestra el diálogo de confirmación si no hay colisiones.

        En la fase de "playing":
        - Si ya se realizó una acción, solo permite clics en el botón "End Turn".
        - Detecta clics en los botones de movimiento del barco seleccionado.
        - Detecta clics en la cuadrícula de posiciones para seleccionar un barco.
        - Detecta clics en la cuadrícula de ataque para realizar un disparo.
        - Detecta clics en el botón "End Turn" para finalizar el turno.
        """
        if self.show_confirmation:
            if self.btnConfirmYes.collidepoint(mouse_pos):
                self.show_confirmation = False
                return "continue"
            elif self.btnConfirmNo.collidepoint(mouse_pos):
                self.show_confirmation = False
                return None
        elif self.state == "setup":
            if self.btnContinue.collidepoint(mouse_pos):
                if not self.has_ship_collisions():
                    self.show_confirmation = True
        elif self.state == "playing":


            # Si ya se realizó una acción, solo permitir finalizar el turno
            if self.action_taken:
                if self.btnEndTurn.collidepoint(mouse_pos):
                    return "end_turn"
                return None

            # Verificar si se hizo clic en los botones de movimiento
            if self.selected_ship:
                if self.btnMoveUp.collidepoint(mouse_pos):
                    return self.move_selected_ship('up')
                elif self.btnMoveDown.collidepoint(mouse_pos):
                    return self.move_selected_ship('down')
                elif self.btnMoveLeft.collidepoint(mouse_pos):
                    return self.move_selected_ship('left')
                elif self.btnMoveRight.collidepoint(mouse_pos):
                    return self.move_selected_ship('right')

            # Verificar si se hizo clic en el tablero de posiciones para seleccionar un barco
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x1 + col * self.cellSz
                    y = self.offset_y1 + row * self.cellSz
                    position_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)

                    if position_rect.collidepoint(mouse_pos):
                        return self.handle_ship_selection(row, col)

            # Check if the click is on the attack grid
            for row in range(self.gridSz):
                for col in range(self.gridSz):
                    x = self.offset_x2 + col * self.cellSz
                    y = self.offset_y2 + row * self.cellSz
                    attack_rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                    if attack_rect.collidepoint(mouse_pos):
                        # Deseleccionar barco al atacar
                        self.selected_ship = None
                        return self.handle_attack(mouse_pos, row, col)

            # Check if the click is on the End Turn button
            if self.btnEndTurn.collidepoint(mouse_pos):
                if self.action_taken or self.game_over:
                    # Deseleccionar barco al finalizar turno
                    self.selected_ship = None
                    return "end_turn"
        return None

    def handle_ship_selection(self, row, col):
        """
        Maneja la selección de un barco por parte del jugador haciendo clic en la cuadrícula de posiciones.

        - Itera a través de los barcos del jugador.
        - Si las coordenadas del clic (`row`, `col`) coinciden con la posición de algún segmento de un barco:
            - Si el barco ya estaba seleccionado (`self.selected_ship`), lo deselecciona (`self.selected_ship = None`).
            - Si el barco no estaba seleccionado, lo selecciona (`self.selected_ship = ship`) y retorna la cadena "ship_selected".
        - Si las coordenadas del clic no coinciden con ningún barco, deselecciona cualquier barco que estuviera previamente seleccionado (`self.selected_ship = None`) y retorna `None`.
        """
        # Verificar si hay un barco en la posición seleccionada
        for ship in self.player.ships:
            if (row, col) in ship.position:
                # Si ya estaba seleccionado, deseleccionarlo
                if self.selected_ship == ship:
                    self.selected_ship = None
                else:
                    self.selected_ship = ship
                return "ship_selected"

        # Si no hay barco, deseleccionar
        self.selected_ship = None
        return None

    def move_selected_ship(self, direction):
        """
        Intenta mover el barco actualmente seleccionado en la dirección especificada.

        - Primero, verifica si hay un barco seleccionado y si el jugador ya realizó una acción en este turno. Si no hay barco o ya se actuó, retorna `None`.
        - Luego, verifica si el barco seleccionado puede moverse según las reglas de daño utilizando `self.can_ship_move()`. Si no puede moverse debido al daño, muestra un mensaje de colisión y retorna `None`.
        - Guarda las posiciones originales del barco antes de intentar moverlo.
        - Verifica si el barco puede moverse en la `direction` dada dentro de los límites de la cuadrícula y sin colisionar con otros barcos del jugador usando `self.selected_ship.can_move()`.
        - Si el movimiento es posible:
            - Registra las posiciones dañadas del barco antes de moverlo en `self.damaged_positions`.
            - Llama al método `move()` del barco seleccionado para actualizar su posición.
            - Llama a `self.update_player_board()` para reflejar el nuevo estado del tablero.
            - Marca `self.action_taken` como `True` para indicar que el jugador ya realizó una acción.
            - Retorna la cadena "ship_moved".
        - Si el movimiento no es posible, muestra un mensaje de colisión indicando que no se puede mover en esa dirección y retorna `None`.
        """
        if not self.selected_ship or self.action_taken:
            return None

        # Verificar si el barco puede moverse según las reglas de daño
        if not self.can_ship_move(self.selected_ship):
            self.collision_message = "Daño en el motor"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None

        # Guardar las posiciones actuales del barco antes de moverlo
        old_positions = self.selected_ship.position.copy()

        # Verificar si el barco puede moverse en esa dirección
        if self.selected_ship.can_move(direction, self.gridSz, self.player.ships):
            # Registrar las posiciones dañadas antes de mover
            for idx, pos in enumerate(old_positions):
                if self.selected_ship.damage_positions[idx]:
                    self.damaged_positions.add(pos)

            # Mover el barco
            self.selected_ship.move(direction)

            # Actualizar el tablero del jugador
            self.update_player_board()

            # Marcar que se ha realizado una acción
            self.action_taken = True

            return "ship_moved"
        else:
            # Mostrar mensaje de que no se puede mover
            self.collision_message = "No se puede mover el barco en esa dirección"
            self.message_timer = pygame.time.get_ticks() + 2000
            return None

    def clear_shots_at_ship_positions(self, ship):
        """
        Elimina las posiciones de un barco dado del historial de disparos (hits y misses) tanto del jugador como del oponente.

        - Itera a través de cada posición (`pos`) del barco.
        - Para cada posición:
            - Si `pos` está en la lista de `self.opponent.hits`, lo elimina. También lo elimina de `self.hits` si está presente.
            - Si `pos` está en la lista de `self.opponent.misses`, lo elimina. También lo elimina de `self.misses` si está presente.
        """
        for pos in ship.position:
            # Eliminar de hits si existe
            if pos in self.opponent.hits:
                self.opponent.hits.remove(pos)
                if pos in self.hits:
                    self.hits.remove(pos)

            # Eliminar de misses si existe
            if pos in self.opponent.misses:
                self.opponent.misses.remove(pos)
                if pos in self.misses:
                    self.misses.remove(pos)

    def apply_auto_damage_if_hit(self, ship):
        """
        Verifica si alguna parte de la nueva posición de un barco coincide con un disparo exitoso previo del oponente y aplica daño automáticamente.

        - Itera a través de cada índice (`idx`) y posición (`pos`) del barco.
        - Si la `pos` actual del barco se encuentra en el historial de `self.opponent.hits`:
            - Si la parte del barco en ese índice (`ship.damage_positions[idx]`) no estaba ya dañada:
                - Marca esa parte como dañada (`ship.damage_positions[idx] = True`).
                - Reduce la vida del barco (`ship.life -= 1`).
                - Añade la `pos` al conjunto de `self.damaged_positions` para su representación visual.
        """
        for idx, pos in enumerate(ship.position):
            # Si la posición está en el historial de hits del oponente, aplicar daño
            if pos in self.opponent.hits:
                if not ship.damage_positions[idx]:  # Solo si no estaba ya dañada
                    ship.damage_positions[idx] = True
                    ship.life -= 1  # Reducir la vida del barco
                    # Añadir a las posiciones dañadas
                    self.damaged_positions.add(pos)

    def check_for_damage_after_move(self, ship):
        pass

    def can_ship_move(self, ship):
        """
        Determina si un barco puede moverse basándose en su estado de daño.

        - Si la vida del barco es igual a su longitud (no ha recibido daño), retorna `True`.
        - Si la longitud del barco es 1, no puede moverse si ha recibido algún daño, por lo que retorna `False`.
        - Para barcos de mayor longitud, verifica si alguna de las posiciones internas (no en los extremos) está dañada. Si alguna posición interna está dañada, retorna `False`.
        - Si solo los extremos del barco están dañados (o no está dañado), retorna `True`.
        """
        if ship.life == ship.length:
            return True

        # Para barcos de longitud 1, no pueden moverse si están dañados
        if ship.length == 1:
            return False

        # Para barcos más largos, verificar si el daño está en posiciones internas
        for idx in range(1, ship.length - 1):  # Posiciones internas (1 a length-2)
            if ship.damage_positions[idx]:
                return False  # No puede moverse si hay daño en posiciones internas

        # Si solo hay daño en los extremos, puede moverse
        return True

    def update_player_board(self):
        """
        Actualiza la representación del tablero del jugador (`self.player.board.grid`) basándose en la posición actual de sus barcos y los disparos fallidos del oponente.

        - Inicializa una nueva cuadrícula del tamaño del tablero del jugador llena de 'w' (agua).
        - Itera a través de los disparos fallidos (`self.opponent.misses`) del oponente y marca esas posiciones como 'o' en la cuadrícula del jugador, siempre y cuando no haya un barco en esa posición.
        - Itera a través de los barcos del jugador y marca la posición de cada segmento en la cuadrícula:
            - Si un segmento está dañado (`ship.damage_positions[idx]` es `True`), lo marca como 'x'.
            - Si un segmento no está dañado, lo marca como 's' (ship).
        """
        # Limpiar el tablero
        self.player.board.grid = [['w' for _ in range(self.player.board.size)] for _ in range(self.player.board.size)]

        # Marcar las posiciones de disparos fallidos como 'o'
        if hasattr(self.opponent, 'misses'):
            for row, col in self.opponent.misses:
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Solo marcar como 'o' si no hay un barco en esa posición
                    if (row, col) not in [pos for ship in self.player.ships for pos in ship.position]:
                        self.player.board.grid[row][col] = 'o'

        # Actualizar posiciones de los barcos en el tablero
        for ship in self.player.ships:
            for idx, (row, col) in enumerate(ship.position):
                if 0 <= row < self.player.board.size and 0 <= col < self.player.board.size:
                    # Marcar como 's' si no está dañada, o como 'x' si está dañada
                    if ship.damage_positions[idx]:
                        self.player.board.grid[row][col] = 'x'  # Parte dañada del barco
                    else:
                        self.player.board.grid[row][col] = 's'  # Parte intacta del barco

    def handle_attack(self, mouse_pos, row, col):
        """
        Maneja la acción de ataque del jugador al hacer clic en la cuadrícula de ataque del oponente.

        - Primero, verifica si el jugador ya realizó una acción en este turno, si el jugador o el oponente no existen, o si el juego terminó. Si alguna de estas condiciones es verdadera, retorna `None`.
        - Dependiendo de la opción `self.option_allow_reshoot`:
            - Si es `True`, permite disparar nuevamente a la misma posición solo si no hay un barco en esa posición. Si ya se disparó a una posición sin barco, no permite disparar de nuevo.
            - Si es `False` (comportamiento original), no permite disparar a ninguna posición que ya haya sido atacada (ya sea un hit o un miss).
        - Si el disparo es válido, utiliza el método `shoot_at_opponent()` de la clase `Player` para registrar el ataque.
        - Si el resultado del disparo es "Disparo exitoso":
            - Añade las coordenadas del impacto (`row`, `col`) a la lista de `self.hits`.
            - Registra la posición dañada en el oponente (si el oponente tiene el atributo `damaged_positions`).
        - Si el disparo no es exitoso (es un miss):
            - Añade las coordenadas del disparo (`row`, `col`) a la lista de `self.misses`.
        - Llama a `self.game_logic.check_victory()` para verificar si el juego ha terminado. Si hay un ganador, actualiza `self.game_over` y `self.winner`.
        - Marca `self.action_taken` como `True` y `self.shot_made` como `True` para indicar que el jugador realizó un disparo en este turno.
        - Retorna la cadena "shot_made".
        """
        # Don't allow shooting if a shot has already been made this turn
        if self.action_taken or not self.player or not self.opponent or self.game_over:
            return None

        if self.option_allow_reshoot:
            # Verificar si hay un barco en la posición
            has_ship = False
            ship_already_damaged = False
            target_ship = None
            position_index = -1
            for ship in self.opponent.ships:
                if (row, col) in ship.position:
                    has_ship = True
                    target_ship = ship
                    position_index = ship.position.index((row, col))
                    # Verificar si esa parte del barco ya está dañada
                    if position_index >= 0 and ship.damage_positions[position_index]:
                        ship_already_damaged = True
                    break

            # Si hay un barco, la posición está en misses, y esa parte del barco NO está dañada, permitir re-atacar
            if has_ship and (row, col) in self.misses and not ship_already_damaged:
                # Remover de la lista de misses ya que ahora será un hit
                self.misses.remove((row, col))
            # Si no hay barco, ya es un hit, o esa parte del barco ya está dañada, no permitir re-atacar
            elif (row, col) in self.hits or (row, col) in self.misses:
                return None

        # Use Player class to shoot at opponent
        result = self.player.shoot_at_opponent(self.opponent, row, col)

        if result == "Disparo exitoso":
            self.hits.append((row, col))

            # Registrar la posición dañada en el oponente
            for ship in self.opponent.ships:
                if (row, col) in ship.position:
                    # Añadir a las posiciones dañadas del oponente
                    if hasattr(self.opponent, 'damaged_positions'):
                        self.opponent.damaged_positions.add((row, col))
                    break
        else:
            self.misses.append((row, col))

        # Check for win condition using GameLogic
        victory_message = self.game_logic.check_victory()
        if victory_message:
            self.game_over = True
            self.winner = f"Player {self.player_number}"

        # Set the action_taken flag to true
        self.action_taken = True
        self.shot_made = True
        return "shot_made"

    def reset_shot_flag(self):
        """
        Restablece la bandera `shot_made` a False, permitiendo al jugador realizar un nuevo disparo en su turno.
        """
        self.shot_made = False
        self.action_taken = False
        self.selected_ship = None
```

### ship.py

**Rol**: Representa un barco en el juego.

**Clase principal:**

- `Ship`: Representa un barco con su posición, orientación y estado.

**Métodos principales:**

1. **`__init__(self, length, x, y, isHorizontal=True, name=None)`**

   - Constructor que inicializa un barco.
   - **Parámetros**:
     - `length`: Longitud del barco
     - `x`: Posición x inicial
     - `y`: Posición y inicial
     - `isHorizontal`: Orientación (True para horizontal)
     - `name`: Nombre del barco

2. **`_calculate_positions(self)`**

   - Calcula todas las posiciones que ocupa el barco.
   - **Retorna**: Lista de tuplas (fila, columna)

3. **`update_positions(self)`**

   - Actualiza las posiciones del barco basado en su posición actual y orientación.

4. **`check_sunken_ship(self)`**

   - Verifica si el barco está hundido.
   - **Retorna**: True si está hundido, False en caso contrario

5. **`damage_received_ship(self, x, y)`**

   - Registra daño en una posición específica del barco.
   - **Parámetros**:
     - `x`: Fila del daño
     - `y`: Columna del daño

6. **`can_move(self, direction, board, other_ships)`**

   - Verifica si el barco puede moverse en una dirección.
   - **Parámetros**:
     - `direction`: Dirección del movimiento ('up', 'down', 'left', 'right')
     - `board`: Tamaño del tablero
     - `other_ships`: Lista de otros barcos para verificar colisiones
   - **Retorna**: True si puede moverse, False en caso contrario

7. **`move(self, direction)`**

   - Mueve el barco en una dirección.
   - **Parámetros**:
     - `direction`: Dirección del movimiento

8. **`check_collision(self, other_ships)`**

   - Verifica colisiones con otros barcos.
   - **Parámetros**:
     - `other_ships`: Lista de otros barcos
   - **Retorna**: True si hay colisión, False en caso contrario

9. **`handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10, other_ships=None)`**

   - Maneja eventos de arrastre y rotación del barco.
   - **Parámetros**:
     - `event`: Evento de pygame
     - `offset_x`: Desplazamiento x del tablero
     - `offset_y`: Desplazamiento y del tablero
     - `cellSize`: Tamaño de cada celda
     - `gridSize`: Tamaño del tablero
     - `other_ships`: Lista de otros barcos

10. **`rotate(self, gridSize)`**

    - Rota el barco (cambia entre horizontal y vertical).
    - **Parámetros**:
      - `gridSize`: Tamaño del tablero

11. **`draw(self, surface, offset_x, offset_y, cellSize)`**
    - Dibuja el barco en una superficie.
    - **Parámetros**:
      - `surface`: Superficie de pygame donde dibujar
      - `offset_x`: Desplazamiento x
      - `offset_y`: Desplazamiento y
      - `cellSize`: Tamaño de cada celda

**Variables importantes:**

- `length`: Longitud del barco
- `x`, `y`: Posición del barco
- `life`: Vida restante del barco
- `isHorizontal`: Orientación del barco
- `name`: Nombre del barco
- `position`: Lista de posiciones que ocupa el barco
- `damage_positions`: Lista que indica qué segmentos están dañados
- `dragging`: Indica si el barco está siendo arrastrado
- `offset_x`, `offset_y`: Desplazamiento durante el arrastre
- `is_colliding`: Indica si el barco está colisionando con otro

```
import pygame

class Ship:
    """
    Representa un barco en el juego Battleship.

    Atributos:
        length (int): La longitud del barco (número de casillas que ocupa).
        x (int): La coordenada x de la posición inicial del barco en la cuadrícula.
        y (int): La coordenada y de la posición inicial del barco en la cuadrícula.
        life (int): La vida actual del barco, igual a su longitud al inicio. Disminuye con los impactos.
        isHorizontal (bool): Indica si el barco está orientado horizontalmente (True) o verticalmente (False).
        name (str, optional): El nombre del barco. Si no se proporciona, se genera automáticamente como "Ship{length}".
        position (list of tuples): Una lista de las coordenadas (y, x) que ocupa el barco en la cuadrícula.
        damage_positions (list of bool): Una lista booleana del mismo tamaño que la longitud del barco, indicando qué segmentos han sido dañados (True).
        dragging (bool): Indica si el barco está siendo arrastrado por el jugador.
        offset_x (int): El desplazamiento x entre la posición del ratón y la esquina superior izquierda del barco durante el arrastre.
        offset_y (int): El desplazamiento y entre la posición del ratón y la esquina superior izquierda del barco durante el arrastre.
        is_colliding (bool): Indica si el barco está actualmente en colisión con otro barco.
        initial_x (int): La coordenada x inicial del barco antes de ser arrastrado.
        initial_y (int): La coordenada y inicial del barco antes de ser arrastrado.
        initial_isHorizontal (bool): La orientación inicial del barco antes de ser arrastrado.
    """
    def __init__(self, length, x, y, isHorizontal=True, name=None):
        """
        Inicializa un nuevo objeto Ship.

        Args:
            length (int): La longitud del barco.
            x (int): La coordenada x inicial del barco.
            y (int): La coordenada y inicial del barco.
            isHorizontal (bool, optional): Indica si el barco está horizontal. Por defecto es True.
            name (str, optional): El nombre del barco. Por defecto es None.
        """
        self.length = length
        self.x = x
        self.y = y
        self.life = length
        self.isHorizontal = isHorizontal
        self.name = name or f"Ship{length}"
        self.position = self._calculate_positions()
        self.damage_positions = [False] * self.length  # Indica qué segmentos del barco están dañados

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
        """
        Calcula la lista de posiciones (y, x) que ocupa el barco en la cuadrícula basándose en su posición, longitud y orientación.

        Returns:
            list of tuples: Una lista de coordenadas (y, x) que representan la posición del barco.
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
        Actualiza la lista de posiciones del barco llamando a `_calculate_positions()` y restablece la bandera de colisión.
        """
        self.position = self._calculate_positions()
        self.is_colliding = False

    def check_sunken_ship(self):
        """
        Verifica si el barco ha sido hundido (su vida es 0).
        """
        return self.life == 0

    def damage_received_ship(self, x, y):
        """
        Registra que el barco ha recibido un impacto en una posición específica.

        Args:
            x (int): La coordenada x del impacto.
            y (int): La coordenada y del impacto.
        """
        for idx, pos in enumerate(self.position):
            if pos[0] == x and pos[1] == y:
                self.damage_positions[idx] = True
                self.life -= 1
                break

    def can_move(self, direction, board, other_ships):
        """
        Verifica si el barco puede moverse en una dirección dada sin salirse del tablero o colisionar con otros barcos.

        Args:
            direction (str): La dirección del movimiento ('left', 'right', 'up', 'down').
            board (int): El tamaño del tablero de juego.
            other_ships (list of Ship): Una lista de otros barcos en el juego.

        Returns:
            bool: True si el barco puede moverse en la dirección especificada, False en caso contrario.
        """
        if self.check_sunken_ship():
            return False

        # Calcular nuevas posiciones según la dirección
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

        # Verificar colisiones con otros barcos
        for ship in other_ships:
            if ship == self: continue
            if set(new_pos).intersection(set(ship.position)):
                return False

        return True

    def move(self, direction):
        """
        Mueve el barco en la dirección especificada y actualiza sus posiciones.

        Args:
            direction (str): La dirección del movimiento ('left', 'right', 'up', 'down').
        """
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
        """
        Verifica si el barco colisiona con alguno de los otros barcos proporcionados.

        Args:
            other_ships (list of Ship): Una lista de otros barcos para verificar colisiones.

        Returns:
            bool: True si hay una colisión, False en caso contrario.
        """
        my_positions = set(self.position)

        for other_ship in other_ships:
            if self == other_ship:
                continue

            other_positions = set(other_ship.position)

            if my_positions.intersection(other_positions):
                return True

        return False

    def handle_event(self, event, offset_x, offset_y, cellSize, gridSize=10, other_ships=None):
        """
        Maneja los eventos de Pygame para permitir arrastrar, soltar y rotar el barco durante la fase de configuración.

        Args:
            event (pygame.event.Event): El evento de Pygame a manejar.
            offset_x (int): El desplazamiento x de la cuadrícula en la superficie.
            offset_y (int): El desplazamiento y de la cuadrícula en la superficie.
            cellSize (int): El tamaño de cada celda de la cuadrícula.
            gridSize (int, optional): El tamaño de la cuadrícula. Por defecto es 10.
            other_ships (list of Ship, optional): Una lista de otros barcos para la detección de colisiones. Por defecto es None.
        """
        if other_ships is None:
            other_ships = []

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
                self.initial_x = self.x #save initial position
                self.initial_y = self.y
                self.initial_isHorizontal = self.isHorizontal

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
                    self.is_colliding = True
                    self.x = self.initial_x #if collide, set positions to initial positions before drag the ship
                    self.y = self.initial_y
                    self.isHorizontal = self.initial_isHorizontal
                    self.update_positions()
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

            self.rotate(gridSize)
            self.update_positions()

            if other_ships and self.check_collision(other_ships):
                self.update_positions()
                self.is_colliding = True
            else:
                self.is_colliding = False

    def rotate(self, gridSize):
        """
        Rota el barco 90 grados y ajusta su posición si es necesario para mantenerlo dentro de la cuadrícula.

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
        Dibuja el barco en la superficie proporcionada.

        Args:
            surface (pygame.Surface): La superficie en la que se dibujará el barco.
            offset_x (int): El desplazamiento x de la cuadrícula.
            offset_y (int): El desplazamiento y de la cuadrícula.
            cellSize (int): El tamaño de cada celda.
        """
        color = (255, 0, 0) if self.is_colliding else (0, 0, 0)

        if self.isHorizontal:
            for i in range(self.length):
                x = offset_x + (self.x + i) * cellSize
                y = offset_y + self.y * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)

                # Dibujar el segmento del barco
                segment_color = (255, 0, 0) if self.damage_positions[i] else color
                pygame.draw.rect(surface, segment_color, rect)
        else:
            for i in range(self.length):
                x = offset_x + self.x * cellSize
                y = offset_y + (self.y + i) * cellSize
                rect = pygame.Rect(x, y, cellSize, cellSize)

                # Dibujar el segmento del barco
                segment_color = (255, 0, 0) if self.damage_positions[i] else color
                pygame.draw.rect(surface, segment_color, rect)
```

### window.py

**Rol**: Maneja la ventana principal del juego y los elementos del menú.

**Clase principal:**

- `Window`: Representa la ventana principal del juego.
  - `__init__`: Inicializa la ventana con dimensiones y título.
  - `drawBtns`: Dibuja los botones del menú principal (Play y Exit).
  - `renderSurface`: Muestra una superficie en la ventana.
  - `updateWindow`: Actualiza la pantalla.

**Variables importantes:**

- `btnPlay`, `btnExit`: Rectángulos que representan los botones del menú.
- `back`: Imagen de fondo del menú.

```
import pygame

class Window:
    """
    Representa la ventana principal del juego.

    Atributos:
        width (int): El ancho de la ventana en píxeles.
        height (int): La altura de la ventana en píxeles.
        title (str): El título de la ventana.
        window (pygame.Surface): La superficie de la ventana principal de Pygame.
        font (pygame.font.Font): La fuente utilizada para el título.
        font_button (pygame.font.Font): La fuente utilizada para los botones.
        back (pygame.Surface): La imagen de fondo de la ventana.
        btnPlay (pygame.Rect): El rectángulo que define el botón "Play".
        btnExit (pygame.Rect): El rectángulo que define el botón "Exit".
    """
    def __init__(self, width, height, title):
        """
        Inicializa la ventana del juego.

        Args:
            width (int): El ancho de la ventana.
            height (int): La altura de la ventana.
            title (str): El título de la ventana.
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.window.fill((0, 128, 255))


        self.font = pygame.font.Font(None, 100)
        self.font_button= pygame.font.Font(None, 36)
        self.back=pygame.image.load("6292.jpg")
        self.back = pygame.transform.scale(self.back, (self.width, self.height))
        self.btnPlay = pygame.Rect(350, 250, 100, 50)
        self.btnExit = pygame.Rect(350, 350, 100, 50)



    def drawBtns(self):
        """
        Dibuja los botones "Play" y "Exit" en la ventana. También dibuja la imagen de fondo y el título.
        """
        self.window.fill((3, 37, 108))
        self.window.blit(self.back, (0,0))


        title = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.window.blit(title, title_rect)

        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay)
        pygame.draw.rect(self.window, (255, 0, 0), self.btnExit)

        play_text = self.font_button.render('Play', True, (255, 255, 255))
        exit_text = self.font_button.render('Exit', True, (255, 255, 255))

        play_rect = play_text.get_rect(center=self.btnPlay.center)
        exit_rect = exit_text.get_rect(center=self.btnExit.center)

        self.window.blit(play_text, play_rect)
        self.window.blit(exit_text, exit_rect)

    def renderSurface(self, surface):
        """
        Renderiza una superficie dada en la ventana principal.

        Args:
            surface (pygame.Surface): La superficie a renderizar.
        """
        self.window.blit(surface, (0, 0))

    def updateWindow(self):
        """
        Actualiza la ventana para mostrar los cambios realizados.
        """
        pygame.display.update()


```

## Views

### main.py

**Rol**: Punto de entrada principal del juego, maneja la navegación entre pantallas y la lógica principal del flujo del juego.

**Componentes principales:**

- `game()`: Función principal que inicializa el juego.
  - Crea la ventana principal y las superficies de juego.
  - Maneja el bucle principal del juego.
  - Controla la transición entre pantallas (menú principal, configuración de barcos, juego).
  - Gestiona el cambio de turnos entre jugadores.

**Variables importantes:**

- `window`: Instancia de la clase Window para la ventana principal.
- `surfacePlayer1`, `surfacePlayer2`: Instancias de GameSurface para cada jugador.
- `current_surface`: Controla qué pantalla se está mostrando actualmente.
- `game_started`: Bandera que indica si el juego ha comenzado.

```
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pygame
from src.Models.window import Window
from src.Models.gameSurface import GameSurface

def game():
    """
    Función principal que inicializa y ejecuta el juego.

    - Inicializa Pygame.
    - Crea una ventana para el juego.
    - Dibuja los botones iniciales en la ventana principal (Play, Exit).
    - Crea dos instancias de GameSurface, una para cada jugador, para la fase de colocación de barcos y el juego.
    - Entra en el bucle principal del juego para manejar eventos y actualizar la pantalla.
    - Permite la transición entre las superficies de los jugadores para la colocación de barcos.
    - Inicia el juego una vez que ambos jugadores han colocado sus barcos.
    - Cambia entre las superficies de los jugadores durante la fase de juego para los turnos.
    - Permite reiniciar el juego desde la pantalla de Game Over.
    - Sale de Pygame y del sistema al finalizar.
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
