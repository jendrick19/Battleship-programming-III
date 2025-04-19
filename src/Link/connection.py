import socket
import json

class Conexion:
    def __init__(self, modo_servidor: bool, ip: str = "0.0.0.0", puerto: int = 5000, timeout: int = 10):
        self.modo_servidor = modo_servidor
        self.ip = ip
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.canal = None
        self.timeout = timeout  # Tiempo de espera en segundos

        if self.modo_servidor:
            self._iniciar_como_servidor()
        else:
            self._iniciar_como_cliente()

    def _iniciar_como_servidor(self):
        try:
            self.sock.bind((self.ip, self.puerto))
            self.sock.listen(1)
            print(f"[SERVIDOR] Esperando conexión en {self.ip}:{self.puerto}...")
            self.canal, direccion = self.sock.accept()
            print(f"[SERVIDOR] Cliente conectado desde {direccion}")
            self.canal.settimeout(self.timeout)  # Configurar timeout para la recepción
        except Exception as error:
            raise ConnectionError(
                f"[ERROR SERVIDOR] No se pudo iniciar el servidor: {error}"
            )

    def _iniciar_como_cliente(self):
        try:
            self.sock.connect((self.ip, self.puerto))
            self.canal = self.sock
            print(f"[CLIENTE] Conectado al servidor en {self.ip}:{self.puerto}")
            self.canal.settimeout(self.timeout)  # Configurar timeout para la recepción
        except Exception as error:
            raise ConnectionError(
                f"[ERROR CLIENTE] No se pudo conectar al servidor: {error}"
            )

    def enviar_datos(self, info: dict):
        try:
            mensaje = json.dumps(info).encode("utf-8")
            self.canal.sendall(mensaje)
            print(f"[ENVÍO] Datos enviados: {info}")
        except Exception as error:
            print(f"[ERROR ENVÍO] {error}")

    def recibir_datos(self) -> dict:
        try:
            datos = self.canal.recv(1024).decode("utf-8")
            if not datos:
                raise Exception("[ERROR RECEPCIÓN] No se recibieron datos.")
            return json.loads(datos)
        except socket.timeout:
            print(f"[ERROR RECEPCIÓN] Tiempo de espera agotado. No se recibió respuesta.")
            return {}
        except Exception as error:
            print(f"[ERROR RECEPCIÓN] {error}")
            return {}

    def finalizar(self):
        try:
            if self.canal:
                self.canal.close()
            self.sock.close()
            print("[CONEXIÓN] Cerrada exitosamente")
        except Exception as error:
            print(f"[ERROR AL CERRAR] {error}")
