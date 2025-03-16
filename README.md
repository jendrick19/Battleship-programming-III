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
    Models/
        playingSurface.py
        ship.py
        surface.py
        window.py
    Views/
        main.py
```

### window.py

```
import pygame

"""
    Clase para gestionar la ventana principal del juego.

    Atributos:
        width (int): Ancho de la ventana en píxeles.
        height (int): Alto de la ventana en píxeles.
        title (str): Título de la ventana.
        window (pygame.Surface): Objeto Surface que representa la ventana.
        font (pygame.font.Font): Fuente utilizada para el texto en la ventana.
        btnPlay (pygame.Rect): Objeto Rect que define la posición y tamaño del botón "Play".
        btnExit (pygame.Rect): Objeto Rect que define la posición y tamaño del botón "Exit".
"""

class Window:
    def __init__(self, width, height, title):
        """
        Inicializa la ventana del juego.

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
        self.titleMenu = pygame.Rect(350,100,100,50)
        self.btnPlay = pygame.Rect(350,300,100,50) # Rectángulo para el botón "Play"
        self.btnExit = pygame.Rect(350,355,100,50) # Rectángulo para el botón "Exit"
        self.font = pygame.font.Font(None,36)

    def updateWindow(self):
        """Actualiza la ventana del juego."""
        pygame.display.flip()

    def getWindow(self):
        """Obtiene la ventana del juego."""
        return self.window

    def renderSurface(self,surface):
        """
        Dibuja una superficie dada en la ventana.

        Args:
            surface (pygame.Surface): La superficie que se va a dibujar.
        """
         self.window.blit(surface, (0,0)) # Dibuja la superficie en la posición (0, 0) de la ventana

    def drawBtns(self):
        """
        Dibuja los botones "Play" y "Exit" en la ventana.

        También dibuja el título del juego en la parte superior.
        """
        titleMenu = self.font.render("BATTLESHIP", True, (255, 255, 255)) # Renderiza el título en blanco
        rectTitleMenu = titleMenu.get_rect(center=self.titleMenu.center) # Centra el título en la parte superior

        self.window.blit(titleMenu,rectTitleMenu) # Dibuja el título en la ventana

        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay) # Dibuja el botón "Play" en rojo
        pygame.draw.rect(self.window, (0, 0, 255), self.btnExit) # Dibuja el botón "Exit" en rojo

        textPlay = self.font.render('PLAY', True, (255, 255, 255)) # Renderiza el texto "Play" en blanco
        textExit = self.font.render('EXIT', True, (255, 255, 255)) # Renderiza el texto "Exit" en blanco

        rectPlay = textPlay.get_rect(center=self.btnPlay.center) # Centra el texto "Play" en el botón
        rectExit = textExit.get_rect(center=self.btnExit.center) # Centra el texto "Exit" en el botón

        self.window.blit(textPlay, rectPlay) # Dibuja el texto "Play" en el botón
        self.window.blit(textExit, rectExit) # Dibuja el texto "Exit" en el botón


```

### surface.py

```
import pygame
from src.Models.ship import Ship

class Surface:
    """
    Clase para gestionar la superficie donde se dibuja la configuración de los barcos del jugador.

    Atributos:
        widthS (int): Ancho de la superficie en píxeles.
        heightS (int): Alto de la superficie en píxeles.
        title (str): Título de la superficie que se mostrará.
        titleSurface (pygame.Rect): Objeto Rect que define la posición y tamaño del área del título.
        btnContinue (pygame.Rect): Objeto Rect que define la posición y tamaño del botón "Continue".
        btnReset (pygame.Rect): Objeto Rect que define la posición y tamaño del botón "Reset".
        surface (pygame.Surface): Objeto Surface donde se dibujan los elementos.
        gridSz (int): Tamaño de la cuadrícula (lado x lado).
        cellSz (int): Tamaño de cada celda de la cuadrícula en píxeles.
        xGrid (int): Ancho total de la cuadrícula en píxeles.
        offset_x (int): Desplazamiento horizontal de la cuadrícula desde el borde izquierdo de la superficie.
        offset_y (int): Desplazamiento vertical de la cuadrícula desde el borde superior de la superficie.
        gridP (list[list[str]]): Representación matricial de la cuadrícula del jugador.
        ships (list[Ship]): Lista de objetos Ship que representan los barcos del jugador.
        font (pygame.font.Font): Fuente utilizada para el texto en la superficie.
    """
    def __init__(self, title, widthS, heightS):
        """
        Inicializa la superficie para la configuración de los barcos.

        Args:
            title (str): Título que se mostrará en la superficie.
            widthS (int): Ancho deseado para la superficie.
            heightS (int): Alto deseado para la superficie.
        """
        pygame.font.init() # Inicializa el módulo de fuentes de Pygame
        self.widthS = widthS
        self.heightS = heightS
        self.title = title

        self.titleSurface = pygame.Rect(350, 25, 100, 50) # Rectángulo para el título de la superficie
        self.btnContinue = pygame.Rect(250, 545, 90, 50) # Rectángulo para el botón "Continue"
        self.btnReset = pygame.Rect(490, 545, 60, 50)  # Rectángulo para el botón "Reset"

        self.surface = pygame.Surface((widthS, heightS))
        self.surface.fill((0, 128, 255))

        self.gridSz = 10 # Tamaño de la cuadrícula 10x10
        self.cellSz = 30 # Cada celda tiene 30x30 píxeles
        self.xGrid = self.gridSz * self.cellSz # Ancho total de la cuadrícula
        self.offset_x, self.offset_y = 50, 100 # Desplazamiento de la cuadrícula
        self.gridP = None # Inicialmente la cuadrícula del jugador está vacía

        self.ships = [Ship(4, 0, 0), Ship(3, 0, 2), Ship(2, 0, 4)] # Crea instancias de los barcos del jugador
                        # (longitud, posición inicial x, posición inicial y)
        self.font = pygame.font.Font(None, 24) # Fuente predeterminada de Pygame, tamaño 24

    def create_Player_Grid(self):
        """
        Crea una representación matricial de la cuadrícula del jugador, inicialmente vacía.
        """
        self.gridP = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]

    def drawGrid(self):
        """
        Dibuja las líneas de la cuadrícula en la superficie.
        """
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

    def drawShips(self):
        """
        Dibuja los barcos del jugador en la superficie y actualiza la representación matricial de la cuadrícula.
        """
        self.gridP = [[' ' for _ in range(self.gridSz)] for _ in range(self.gridSz)]
        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)
            for i in range(ship.length):
                row = int(ship.y)
                col = int(ship.x + i)
                if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
                    self.gridP[row][col] = 'S'

    def updateWindow(self):
        """
        Actualiza la ventana.
        """
        pygame.display.flip()

    def drawBtn(self):
        """
        Dibuja el título de la superficie y los botones "Continue" y "Reset".
        """
        title = self.font.render(self.title, True, (255, 255, 255))
        rectTitle = title.get_rect(center=self.titleSurface.center) # Centra el título en su rectángulo
        self.surface.blit(title, rectTitle) # Dibuja el título en la superficie

        pygame.draw.rect(self.surface, (255, 0, 0), self.btnContinue) # Dibuja el botón "Continue" en rojo
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset) # Dibuja el botón "Reset" en rojo

        textContinue = self.font.render('Continue', True, (255, 255, 255)) # Renderiza el texto "Continue" en blanco
        textReset = self.font.render('Reset', True, (255, 255, 255)) # Renderiza el texto "Reset" en blanco

        rectContinue = textContinue.get_rect(center=self.btnContinue.center) # Centra el texto en el botón "Continue"
        rectReset = textReset.get_rect(center=self.btnReset.center) # Centra el texto en el botón "Reset"

        self.surface.blit(textContinue, rectContinue) # Dibuja el texto "Continue" en el botón
        self.surface.blit(textReset, rectReset) # Dibuja el texto "Reset" en el botón

    def handle_events(self, events):
        """
        Maneja los eventos para la superficie, principalmente para la interacción con los barcos.

        Args:
            events (list): Lista de eventos de Pygame a ser procesados.
        """
        for event in events:
            for ship in self.ships:
                ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz)
```
