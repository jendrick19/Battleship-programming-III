import threading
import socket
import time
import logging
from connection import Conexion
from Game import gameLogic, player
from Models import board, ship

logging.basicConfig(level=logging.INFO)

class Servidor:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientes = {} 
        self.game_state = {
            "jugadores": {1: {"barcos": None, "player": None}, 2: {"barcos": None, "player": None}},
            "conexiones": {1: None, 2: None},
            "juego_terminado": False,
            "turno_actual": None
        }
        self.next_player_id = 1

    def iniciar(self):
        try:
            self.servidor_socket.bind((self.host, self.port))
            self.servidor_socket.listen(2)  
            logging.info(f"[SERVIDOR] Esperando conexiones en {self.host}:{self.port}...")
            while len(self.clientes) < 2:
                canal_cliente, direccion_cliente = self.servidor_socket.accept()
                nuevo_conexion = Conexion(modo_servidor=False) 
                nuevo_conexion.canal = canal_cliente
                logging.info(f"[SERVIDOR] Cliente conectado desde {direccion_cliente}")
                player_id = self.next_player_id
                self.clientes[player_id] = nuevo_conexion
                self.game_state["conexiones"][player_id] = nuevo_conexion
                threading.Thread(target=self.manejar_cliente, args=(nuevo_conexion, player_id), daemon=True).start()
                logging.info(f"[SERVIDOR] Asignado ID {player_id} al cliente.")
                self.next_player_id += 1

            logging.info("[SERVIDOR] Ambos jugadores conectados. ¡Partida lista para recibir configuraciones!")
            self._iniciar_juego()

        except socket.error as e:
            logging.error(f"[SERVIDOR] Error al iniciar el servidor: {e}")
        finally:
            self.servidor_socket.close()

    def _iniciar_juego(self):
        import random
        primer_jugador = random.choice([1, 2])
        self.game_state["turno_actual"] = primer_jugador
        for player_id, conexion in self.clientes.items():
            conexion.enviar_datos({"accion": "inicio_juego", "tu_turno": (player_id == self.game_state["turno_actual"])})

    def manejar_cliente(self, conexion_cliente, player_id):
        try:
            barcos_data = conexion_cliente.recibir_datos()
            if not self._validar_datos(barcos_data):
                logging.error(f"[SERVIDOR] Configuración inválida del Jugador {player_id}")
                return

            logging.info(f"[SERVIDOR] Recibida configuración del Jugador {player_id}: {barcos_data['barcos']}")
            player_obj = self._crear_objetos_juego(barcos_data["barcos"], f"Jugador {player_id}")
            self.game_state["jugadores"][player_id]["player"] = player_obj

            while not all(self.game_state["jugadores"][i]["player"] for i in [1, 2]):
                time.sleep(0.1)

            conexion_cliente.enviar_datos({"accion": "configuracion_completa", "turno": (player_id == self.game_state["turno_actual"])})
            otro_jugador_id = 2 if player_id == 1 else 1
            if otro_jugador_id in self.clientes:
                self.clientes[otro_jugador_id].enviar_datos({"accion": "configuracion_completa", "turno": (otro_jugador_id == self.game_state["turno_actual"])})

            while not self.game_state["juego_terminado"]:
                if self.game_state["turno_actual"] == player_id:
                    datos_cliente = conexion_cliente.recibir_datos()
                    if datos_cliente:
                        accion = datos_cliente.get("accion")
                        if accion == "disparo":
                            coordenadas = datos_cliente.get("coordenadas")
                            if coordenadas:
                                fila, columna = coordenadas
                                otro_jugador_id = 2 if player_id == 1 else 1
                                oponente = self.game_state["jugadores"][otro_jugador_id]["player"]
                                if oponente:
                                    resultado = oponente.recibir_disparo(fila, columna)
                                    conexion_cliente.enviar_datos({
                                        "accion": "resultado_propio",
                                        "fila": fila,
                                        "columna": columna,
                                        "resultado": resultado
                                    })
                                    conexion_oponente = self.game_state["conexiones"][otro_jugador_id]
                                    if conexion_oponente:
                                        conexion_oponente.enviar_datos({
                                            "accion": "recibir_disparo",
                                            "fila": fila,
                                            "columna": columna,
                                            "impacto": resultado
                                        })
                                    if oponente.ha_perdido():
                                        self.game_state["juego_terminado"] = True
                                        ganador = f"Jugador {player_id}"
                                        conexion_cliente.enviar_datos({"accion": "fin_partida", "ganador": ganador})
                                        if conexion_oponente:
                                            conexion_oponente.enviar_datos({"accion": "fin_partida", "ganador": ganador})
                                    else:
                                        self.game_state["turno_actual"] = otro_jugador_id
                                        conexion_oponente.enviar_datos({"accion": "turno", "es_tu_turno": True})
                                        conexion_cliente.enviar_datos({"accion": "turno", "es_tu_turno": False})
                                else:
                                    logging.error("[SERVIDOR] ¡Error! No se encontró al oponente.")
                            else:
                                logging.error("[SERVIDOR] ¡Error! Coordenadas de disparo inválidas.")
                    else:
                        logging.warning(f"[SERVIDOR] El Jugador {player_id} se desconectó.")
                        self._limpiar_cliente(player_id)
                        break
                else:
                    time.sleep(0.1)  # Evitar CPU alta cuando no es el turno
        except Exception as e:
            logging.error(f"[SERVIDOR] Error al manejar al cliente {player_id}: {e}")
        finally:
            self._limpiar_cliente(player_id)
            conexion_cliente.finalizar()

    def _validar_datos(self, barcos_data):
        return isinstance(barcos_data, dict) and "barcos" in barcos_data

    def _crear_objetos_juego(self, barcos_data, player_name):
        player_obj = player.Player(player_name)
        board_obj = board.Board(10)
        for barco_info in barcos_data:
            ship_obj = ship.Ship(
                barco_info["length"],
                barco_info["x"],
                barco_info["y"],
                barco_info["isHorizontal"],
                barco_info["name"]
            )
            ship_obj.position = barco_info["position"]
            player_obj.add_ship(ship_obj)
            for row, col in ship_obj.position:
                if 0 <= row < board_obj.size and 0 <= col < board_obj.size:
                    board_obj.grid[row][col] = 's'
        player_obj.board = board_obj
        return player_obj

    def _limpiar_cliente(self, player_id):
        if player_id in self.clientes:
            del self.clientes[player_id]
        if player_id in self.game_state["conexiones"]:
            self.game_state["conexiones"][player_id] = None
        if player_id in self.game_state["jugadores"]:
            self.game_state["jugadores"][player_id]["player"] = None
            self.game_state["jugadores"][player_id]["barcos"] = None
        logging.info(f"[SERVIDOR] Datos del Jugador {player_id} limpiados.")

    def _reiniciar_juego(self):
        self.game_state = {
            "jugadores": {1: {"barcos": None, "player": None}, 2: {"barcos": None, "player": None}},
            "conexiones": {1: None, 2: None},
            "juego_terminado": False,
            "turno_actual": None
        }
        self.clientes.clear()
        self.next_player_id = 1
        logging.info("[SERVIDOR] Juego reiniciado.")

def main():
    servidor = Servidor(host="0.0.0.0", port=5000)
    servidor.iniciar()

if __name__ == "__main__":
    main()