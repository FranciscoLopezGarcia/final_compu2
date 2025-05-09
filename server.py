import socket
import threading
from blackjack import Blackjack
from player import Player


HOST = '0.0.0.0'
PORT = 22224

def manejo_cliente(conection, address):
    print(f"Conexión establecida con {address}")
    conection.sendall(b"Conectado al servidor. Ingrese su nombre:\n")

    nombre = conection.recv(1024).decode().strip()
    jugador = Player(nombre)
    juego = Blackjack(jugador)

    conection.sendall(f"Bienvenido {nombre}\n".encode())



    while True:
        try:
            data= conection.recv(1024)
            if not data:
                break

            msj = data.decode().lower()
            if msj == "pedir":
                carta = juego.repartir()
                estado = jugador.get_status()
                rta = f"Carta: {carta}, Total: {estado['total']}, \n Estado: {estado['estado']}, \n"
            else:
                rta = "Comando no reconocido. Intente 'pedir' para recibir una carta.\n"

            conection.sendall(rta.encode())

        except:
            break


    print(f"Cliente {address} desconectado")
    conection.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[INFO] Servidor escuchando en {HOST}:{PORT}")

    while True:
        conection, address = server.accept()
        hilo = threading.Thread(target=manejo_cliente, args=(conection, address))
        hilo.start()

if __name__ == "__main__":
    main()