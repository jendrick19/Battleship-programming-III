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
        self.buffer = ""  # acumulador para el framing con '\n'

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

    def _iniciar_como_cliente(self):
        for intento in range(3):
            try:
                self.sock.connect((self.ip, self.puerto))
                self.canal = self.sock
                logger.info(f"[Cliente] Conectado a {self.ip}:{self.puerto}")
                return
            except Exception as e:
                logger.warning(f"[Cliente] Fallo intento {intento+1}: {e}")
                time.sleep(2 ** intento)
        raise ConnectionError("No se pudo reconectar tras 3 intentos")

    def enviar_datos(self, info: dict):
        try:
            msg = json.dumps(info) + "\n"  # protocolo delimitado
            self.canal.sendall(msg.encode('utf-8'))
            logger.debug(f"[ENVIAR] {info}")
        except Exception as e:
            logger.error(f"[ERROR ENVÍO] {e}")
            raise ConnectionError(f"Error al enviar: {e}")
        
    def _loop_escucha(self):
        while self.escuchando:
            try:
                msg = self.recibir_datos()
                if msg:
                    if msg.get("type") == "ping":
                        self.enviar_datos({"type": "pong"})
                    elif msg.get("type") == "pong":
                        self.ultimo_pong = time.time()
                    else:
                        self.mensajes_recibidos.append(msg)
            except Exception as e:
                logger.warning(f"[LOOP] Error de recepción: {e}")
            time.sleep(0.05)

            # Enviar ping cada 5s
            if time.time() - self.ultimo_ping > 5:
                self.enviar_datos({"type": "ping"})
                self.ultimo_ping = time.time()

            # Si no hay pong en 10s, asumir desconexión
            if time.time() - self.ultimo_pong > 10:
                logger.error("[LOOP] Conexión inactiva. Finalizando.")
                self.finalizar()
                break

    def recibir_datos(self):
        try:
            ready, _, _ = select.select([self.canal], [], [], 0.1)
            if ready:
                datos = self.canal.recv(self.bufsize).decode('utf-8')
                if not datos:
                    return None  # desconexión
                self.buffer += datos

                if '\n' in self.buffer:
                    raw, self.buffer = self.buffer.split('\n', 1)
                    msg = json.loads(raw)
                    logger.debug(f"[RECIBIR] {msg}")
                    return msg
        except Exception as e:
            logger.error(f"[ERROR RECEPCIÓN] {e}")
            return None
        return None

    def finalizar(self):
        try:
            if hasattr(self, 'canal'):
                self.canal.close()
            self.sock.close()
            logger.info("[Conexion] Socket cerrado correctamente.")
        except Exception as e:
            logger.warning(f"[Conexion] Error al cerrar socket: {e}")

    def get_mensaje(self):
        if self.mensajes_recibidos:
            return self.mensajes_recibidos.pop(0)
        return None

