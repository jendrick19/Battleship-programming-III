import socket
import threading
import json

class Conexion:
    def __init__(self, modo_servidor=False, ip='localhost', puerto=5000):
        self.modo_servidor = modo_servidor
        self.ip = ip
        self.puerto = puerto
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion = None  # Solo se usará en modo servidor
        self.direccion = None

        if self.modo_servidor:
            self.socket.bind((self.ip, self.puerto))
            self.socket.listen(1)
            print(f"[SERVIDOR] Esperando conexión en {self.ip}:{self.puerto}...")
            self.conexion, self.direccion = self.socket.accept()
            print(f"[SERVIDOR] Conectado con {self.direccion}")
        else:
            try:
                self.socket.connect((self.ip, self.puerto))
                print(f"[CLIENTE] Conectado a {self.ip}:{self.puerto}")
            except socket.error as e:
                print(f"[CLIENTE] Error al conectar con el servidor: {e}")
                raise ConnectionError("No se pudo conectar con el servidor")

    def enviar_datos(self, datos):
        try:
            mensaje = json.dumps(datos).encode('utf-8')
            if self.modo_servidor:
                self.conexion.sendall(mensaje)
            else:
                self.socket.sendall(mensaje)
        except Exception as e:
            print(f"[CONEXIÓN] Error al enviar datos: {e}")

    def recibir_datos(self):
        try:
            buffer = b''
            while True:
                chunk = (self.conexion if self.modo_servidor else self.socket).recv(4096)
                if not chunk:
                    break
                buffer += chunk
                try:
                    return json.loads(buffer.decode('utf-8'))
                except json.JSONDecodeError:
                    continue  # Aún no se ha recibido el JSON completo
        except Exception as e:
            print(f"[CONEXIÓN] Error al recibir datos: {e}")
            return {}

    def finalizar(self):
        try:
            if self.modo_servidor and self.conexion:
                self.conexion.close()
            self.socket.close()
            print("[CONEXIÓN] Conexión cerrada.")
        except Exception as e:
            print(f"[CONEXIÓN] Error al cerrar conexión: {e}")
