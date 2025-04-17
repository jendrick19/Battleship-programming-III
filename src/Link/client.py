from src.Link.connection import Conexion
import pygame
import json

class Cliente:
    def __init__(self, host, port, game_surface=None):
        self.host = host
        self.port = port
        self.conexion = Conexion(modo_servidor=False, ip=self.host, puerto=self.port)
        self.player_number = None
        self.mi_tablero = [['' for _ in range(10)] for _ in range(10)]
        self.tablero_oponente = [['' for _ in range(10)] for _ in range(10)]
        self.turno = False
        self.juego_iniciado = False
        self.configuracion_enviada = False
        self.game_surface = game_surface

    def conectar(self):
        try:
            self.conexion.conectar()
            return True
        except ConnectionError as e:
            print(f"[CLIENTE] Error al conectar: {e}")
            return False

    def enviar_configuracion(self, barcos_data):
        try:
            data = {"accion": "configuracion_barcos", "barcos": barcos_data}
            self.conexion.enviar_datos(data)
            self.configuracion_enviada = True
            print("[CLIENTE] Configuración de barcos enviada.")
        except Exception as e:
            print(f"[CLIENTE] Error al enviar configuración: {e}")

    def enviar_disparo(self, fila, columna):
        if self.turno and self.juego_iniciado:
            try:
                data = {"accion": "disparo", "coordenadas": (fila, columna)}
                self.conexion.enviar_datos(data)
                self.turno = False
                print(f"[CLIENTE] Disparo enviado a ({fila}, {columna}).")
                return True
            except Exception as e:
                print(f"[CLIENTE] Error al enviar disparo: {e}")
        elif not self.juego_iniciado:
            print("[CLIENTE] El juego aún no ha comenzado.")
        elif not self.turno:
            print("[CLIENTE] No es tu turno.")
        return False

    def recibir_datos_servidor(self):
        try:
            data = self.conexion.recibir_datos()
            if data:
                self.procesar_datos(data)
            return data
        except Exception as e:
            print(f"[CLIENTE] Error al recibir datos del servidor: {e}")
            return {}

    def procesar_datos(self, data):
        accion = data.get("accion")

        if accion == "inicio_juego":
            self.juego_iniciado = True
            self.turno = data.get("tu_turno", False)
            print(f"[CLIENTE] ¡Juego iniciado! ¿Mi turno? {self.turno}")
            self.mi_tablero = [['' for _ in range(10)] for _ in range(10)]
            self.tablero_oponente = [['' for _ in range(10)] for _ in range(10)]
            if self.game_surface:
                self.game_surface.state = "playing"
                self.game_surface.reset_shot_flag()

        elif accion == "configuracion_completa":
            self.turno = data.get("turno", False)
            print(f"[CLIENTE] Configuración completada. ¿Mi turno inicial? {self.turno}")
            if self.game_surface:
                self.game_surface.reset_shot_flag()

        elif accion == "turno":
            self.turno = data.get("es_tu_turno", False)
            print(f"[CLIENTE] {'Mi turno' if self.turno else 'Turno del oponente'}.")
            if self.game_surface:
                self.game_surface.reset_shot_flag()

        elif accion == "resultado_propio":
            fila = data.get("fila")
            columna = data.get("columna")
            resultado = data.get("resultado")
            if fila is not None and columna is not None:
                if resultado == "Disparo exitoso" or resultado.startswith("Barco hundido"):
                    self.tablero_oponente[fila][columna] = 'X'
                elif resultado == "Disparo fallido":
                    self.tablero_oponente[fila][columna] = 'O'
                if self.game_surface:
                    self.game_surface.actualizar_tablero_oponente(self.tablero_oponente)

        elif accion == "recibir_disparo":
            fila = data.get("fila")
            columna = data.get("columna")
            impacto = data.get("impacto")
            if fila is not None and columna is not None:
                if impacto == "Disparo exitoso" or impacto.startswith("Barco hundido"):
                    self.mi_tablero[fila][columna] = 'x'
                    if self.game_surface:
                        self.game_surface.actualizar_mi_tablero(self.mi_tablero, (fila, columna), True)
                elif impacto == "Disparo fallido":
                    self.mi_tablero[fila][columna] = 'o'
                    if self.game_surface:
                        self.game_surface.actualizar_mi_tablero(self.mi_tablero, (fila, columna), False)
                print(f"[CLIENTE] Recibí disparo en ({fila}, {columna}). Resultado: {impacto}")

        elif accion == "fin_partida":
            ganador = data.get("ganador")
            print(f"[CLIENTE] ¡Partida terminada! El ganador es: {ganador}")
            self.juego_iniciado = False
            if self.game_surface:
                self.game_surface.game_over = True
                self.game_surface.winner = ganador
                self.game_surface.state = "game_over"

        elif accion == "mensaje":
            mensaje = data.get("texto")
            print(f"[CLIENTE] Mensaje del servidor: {mensaje}")

        else:
            print(f"[CLIENTE] Acción desconocida recibida del servidor: {accion}")

    def desconectar(self):
        self.conexion.finalizar()
        print("[CLIENTE] Desconectado.")
