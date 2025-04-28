from src.Link.connection import Conexion

def main():
    ip = input("Ingresa la IP del servidor: ")
    red = Conexion(modo_servidor=False, ip=ip, puerto=5000)

    red.enviar_datos({"mensaje": "Hola desde el cliente"})
    respuesta = red.recibir_datos()
    print("Servidor dice:", respuesta.get("mensaje", "[Sin respuesta]"))

main()