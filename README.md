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
Clase que representa la ventana principal del juego.
"""

class Window:
    def __init__(self, width, height, title):
        """Inicializa la ventana del juego.

        Args:
            width (int): Ancho de la ventana.
            height (int): Alto de la ventana.
            title (str): Título de la ventana.
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.titleMenu = pygame.Rect(350,100,100,50)
        self.btnPlay = pygame.Rect(350,300,100,50)
        self.btnExit = pygame.Rect(350,355,100,50)
        self.font = pygame.font.Font(None,36)

    def updateWindow(self):
        """Actualiza la ventana del juego."""
        pygame.display.flip()

    def getWindow(self):
        """Obtiene la ventana del juego."""
        return self.window

    def renderSurface(self,surface):
        """Renderiza una superficie en la ventana del juego.

        Args:
            surface (pygame.Surface): La superficie a renderizar.
        """
         self.window.blit(surface, (0,0))

    def drawBtns(self):
        """Dibuja los botones en la ventana del juego."""
        titleMenu = self.font.render("BATTLESHIP", True, (255, 255, 255))
        rectTitleMenu = titleMenu.get_rect(center=self.titleMenu.center)

        self.window.blit(titleMenu,rectTitleMenu)

        pygame.draw.rect(self.window, (255, 0, 0), self.btnPlay)
        pygame.draw.rect(self.window, (0, 0, 255), self.btnExit)

        textPlay = self.font.render('PLAY', True, (255, 255, 255))
        textExit = self.font.render('EXIT', True, (255, 255, 255))

        rectPlay = textPlay.get_rect(center=self.btnPlay.center)
        rectExit = textExit.get_rect(center=self.btnExit.center)

        self.window.blit(textPlay, rectPlay)
        self.window.blit(textExit, rectExit)


```

### surface.py

```
import pygame
from src.Models.ship import Ship
from src.Game.board import Board

"""Clase que representa la superficie de juego."""

class Surface:
    def __init__(self, title, widthS, heightS, offset_x, offset_y):
        """Inicializa la superficie de juego.

        Args:
            title (str): Título de la superficie.
            widthS (int): Ancho de la superficie.
            heightS (int): Alto de la superficie.
            offset_x (int): Desplazamiento en el eje x.
            offset_y (int): Desplazamiento en el eje y.
        """
        pygame.font.init()
        self.widthS = widthS
        self.heightS = heightS
        self.title = title

        self.titleSurface = pygame.Rect(350, 25, 100, 50)
        self.btnContinue = pygame.Rect(250, 545, 90, 50)
        self.btnReset = pygame.Rect(490, 545, 60, 50)

        self.surface = pygame.Surface((widthS, heightS))
        self.surface.fill((0, 128, 255))

        self.gridSz = 10
        self.cellSz = 30
        self.xGrid = self.gridSz * self.cellSz
        self.offset_x = offset_x
        self.offset_y= offset_y
        self.gridP = None

        self.ships = [Ship(4, 0, 0, True), Ship(3, 0, 2, True), Ship(2, 0, 4, True)]

        self.font = pygame.font.Font(None, 24)

    def create_Player_Grid(self):
        """Crea la cuadrícula del jugador."""
        self.gridP = Board(self.gridSz)

    def drawGrid(self):
        """Dibuja la cuadrícula en la superficie de juego."""
        for row in range(self.gridSz):
            for col in range(self.gridSz):
                x = self.offset_x + col * self.cellSz
                y = self.offset_y + row * self.cellSz
                rect = pygame.Rect(x, y, self.cellSz, self.cellSz)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

    def drawShips(self):
        """Dibuja los barcos en la superficie de juego."""
        self.gridP = Board(self.gridSz)

        for ship in self.ships:
            ship.draw(self.surface, self.offset_x, self.offset_y, self.cellSz)

            if ship.isHorizontal:
                for i in range(ship.length):
                    row = int(ship.y)
                    col = int(ship.x + i)
                    if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
                        self.gridP.grid[row][col] = 'S'
            else:
                for i in range(ship.length):
                    row = int(ship.y + i)
                    col = int(ship.x)
                    if 0 <= row < self.gridSz and 0 <= col < self.gridSz:
                        self.gridP.grid[row][col] = 'S'

    def updateWindow(self):
        """Actualiza la ventana del juego."""
        pygame.display.flip()

    def drawBtn(self):
        """Dibuja los botones en la superficie de juego."""
        title = self.font.render(self.title, True, (255, 255, 255))
        rectTitle = title.get_rect(center=self.titleSurface.center)
        self.surface.blit(title, rectTitle)

        pygame.draw.rect(self.surface, (255, 0, 0), self.btnContinue)
        pygame.draw.rect(self.surface, (255, 0, 0), self.btnReset)

        textContinue = self.font.render('Continue', True, (255, 255, 255))
        textReset = self.font.render('Reset', True, (255, 255, 255))

        rectContinue = textContinue.get_rect(center=self.btnContinue.center)
        rectReset = textReset.get_rect(center=self.btnReset.center)

        self.surface.blit(textContinue, rectContinue)
        self.surface.blit(textReset, rectReset)

        textRotate = self.font.render('Press SPACE while dragging to rotate', True, (255, 255, 255))
        self.surface.blit(textRotate, (self.offset_x, self.offset_y + self.gridSz * self.cellSz + 10))

    def handle_events(self, events):
        """Maneja los eventos de la superficie de juego.

        Args:
            events (list): Lista de eventos de Pygame.
        """
        for event in events:
            for ship in self.ships:
                ship.handle_event(event, self.offset_x, self.offset_y, self.cellSz, self.gridSz)
```
