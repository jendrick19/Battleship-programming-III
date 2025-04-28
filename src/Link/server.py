from src.Link.connection import Conexion

def main():
    red = Conexion(modo_servidor=True, ip="0.0.0.0", puerto=5000)
    print("Esperando mensajes del cliente...")

    while True:
        datos = red.recibir_datos()
        if not datos:
            print("Cliente desconectado o sin respuesta.")
            break
        print("Cliente dice:", datos["mensaje"])

        red.enviar_datos({"mensaje": "Hola desde el servidor"})

main()