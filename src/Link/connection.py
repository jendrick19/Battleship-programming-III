import socket
import json
import select
import atexit
import threading
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Conexion:
    def __init__(self, modo_servidor=True, ip="0.0.0.0", puerto=5000, backlog=1, bufsize=1024):
        self.ip = ip
        self.puerto = puerto
        self.modo_servidor = modo_servidor
        self.bufsize = bufsize
        self.backlog = backlog
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer = ""
        self.connected = False

        if self.modo_servidor:
            self._iniciar_como_servidor()
        else:
            self._iniciar_como_cliente()

        atexit.register(self.finalizar)

        self.escuchando = True
        self.mensajes_recibidos = []
        self.hilo_escucha = threading.Thread(target=self._loop_escucha, daemon=True)
        self.hilo_escucha.start()

        self.ultimo_ping = time.time()
        self.ultimo_pong = time.time()

    def _iniciar_como_servidor(self):
        self.sock.bind((self.ip, self.puerto))
        self.sock.listen(self.backlog)
        logger.info(f"[Servidor] Esperando conexión en {self.ip}:{self.puerto}...")
        self.canal, addr = self.sock.accept()
        logger.info(f"[Servidor] Conexión aceptada desde {addr}")
        self.connected = True

    def _iniciar_como_cliente(self):
        for intento in range(3):
            try:
                self.sock.connect((self.ip, self.puerto))
                self.canal = self.sock
                self.connected = True
                logger.info(f"[Cliente] Conectado a {self.ip}:{self.puerto}")
                return
            except Exception as e:
                logger.warning(f"[Cliente] Fallo intento {intento + 1}: {e}")
                time.sleep(2 ** intento)
        raise ConnectionError("No se pudo reconectar tras 3 intentos")

    def enviar_datos(self, info: dict):
        if not self.connected:
            logger.error("[ENVIAR] Conexión no activa.")
            raise ConnectionError("No se puede enviar, conexión cerrada.")
        try:
            msg = json.dumps(info) + "\n"
            self.canal.sendall(msg.encode('utf-8'))
            logger.debug(f"[ENVIAR] {info}")
        except (BrokenPipeError, ConnectionAbortedError, OSError) as e:
            logger.error(f"[ERROR ENVÍO] {e}")
            self.finalizar()
            raise ConnectionError(f"Error al enviar: {e}")

    def _loop_escucha(self):
        while self.escuchando and self.connected:
            try:
                msg = self.recibir_datos()
                if msg:
                    if msg.get("type") == "ping":
                        try:
                            self.enviar_datos({"type": "pong"})
                        except ConnectionError as e:
                            logger.error(f"[LOOP] Falló pong: {e}")
                            break
                    elif msg.get("type") == "pong":
                        self.ultimo_pong = time.time()
                    else:
                        self.mensajes_recibidos.append(msg)
            except Exception as e:
                logger.warning(f"[LOOP] Error de recepción: {e}")

            time.sleep(0.05)

            # Ping
            if time.time() - self.ultimo_ping > 5:
                try:
                    self.enviar_datos({"type": "ping"})
                    self.ultimo_ping = time.time()
                except ConnectionError as e:
                    logger.error(f"[LOOP] Ping falló: {e}")
                    self.finalizar()
                    break

            # Timeout
            if time.time() - self.ultimo_pong > 10:
                logger.error("[LOOP] Timeout: oponente inactivo.")
                self.finalizar()
                break

    def recibir_datos(self):
        if not self.connected:
            return None
        try:
            ready, _, _ = select.select([self.canal], [], [], 0.1)
            if ready:
                datos = self.canal.recv(self.bufsize).decode('utf-8')
                if not datos:
                    logger.warning("[RECIBIR] Conexión cerrada por el otro extremo.")
                    self.finalizar()
                    return None
                self.buffer += datos

                while '\n' in self.buffer:
                    raw, self.buffer = self.buffer.split('\n', 1)
                    try:
                        msg = json.loads(raw)
                        logger.debug(f"[RECIBIR] {msg}")
                        return msg
                    except json.JSONDecodeError:
                        logger.warning(f"[RECIBIR] JSON inválido: {raw}")
        except Exception as e:
            logger.error(f"[RECIBIR] Error: {e}")
        return None

    def get_mensaje(self):
        if self.mensajes_recibidos:
            return self.mensajes_recibidos.pop(0)
        return None

    def finalizar(self):
        try:
            if hasattr(self, 'canal'):
                self.canal.close()
            self.sock.close()
            self.connected = False
            logger.info("[Conexion] Socket cerrado correctamente.")
        except Exception as e:
            logger.warning(f"[Conexion] Error al cerrar: {e}")
