import socket
import threading
from blackjack import Blackjack
from player import Player
from mesa import MesaBlackjack

HOST = '0.0.0.0'
PORT = 22224

mesas = {}  # id_mesa -> MesaBlackjack
siguiente_id_mesa = 1
lock_mesas = threading.Lock()

def manejo_cliente(conection, address):
    global siguiente_id_mesa

    print(f"[+] Conexión desde {address}")
    conection.sendall(b"Bienvenido al servidor de Blackjack.\nIngrese su nombre:\n")
    nombre = conection.recv(1024).decode().strip()
    jugador = Player(nombre)

    conection.sendall(b"Comandos:\n[VER_MESAS]\n[CREAR_MESA]\n[UNIRSE_MESA <id>]\n")

    mesa_asignada = None

    while not mesa_asignada:
        try:
            data = conection.recv(1024).decode().strip()
            if data == "VER_MESAS":
                if not mesas:
                    conection.sendall(b"No hay mesas disponibles.\n")
                else:
                    respuesta = "Mesas disponibles:\n"
                    for mid, mesa in mesas.items():
                        jugadores = mesa.get_info_mesa()
                        respuesta += f"ID {mid}: {', '.join(jugadores)}\n"
                    conection.sendall(respuesta.encode())

            elif data == "CREAR_MESA":
                with lock_mesas:
                    mid = siguiente_id_mesa
                    mesas[mid] = MesaBlackjack(mid)
                    siguiente_id_mesa += 1
                mesa_asignada = mesas[mid]
                mesa_asignada.agregar_jugador(conection, jugador)
                conection.sendall(f"Mesa {mid} creada y unida. ¡Empezá a jugar!\n".encode())

            elif data.startswith("UNIRSE_MESA"):
                try:
                    mid = int(data.split()[1])
                    if mid in mesas:
                        mesa_asignada = mesas[mid]
                        mesa_asignada.agregar_jugador(conection, jugador)
                        conection.sendall(f"Unido a la mesa {mid}. ¡Empezá a jugar!\n".encode())
                    else:
                        conection.sendall(b"ID de mesa invalido.\n")
                except:
                    conection.sendall(b"Uso incorrecto. Ej: UNIRSE_MESA 1\n")
            else:
                conection.sendall(b"Comando no reconocido.\n")
        except:
            conection.close()
            return

    # Ciclo de juego
    while True:
        try:
            data = conection.recv(1024)
            if not data:
                break

            msj = data.decode().lower().strip()

            if msj == "pedir":
                carta = mesa_asignada.repartir_a(conection)
                estado = mesa_asignada.get_estado_de(conection)
                rta = f"Carta: {carta}, Total: {estado['total']}, Estado: {estado['estado']}\n"
            elif msj == "ver_mano":
                estado = mesa_asignada.get_estado_de(conection)
                rta = f"Mano: {estado['mano']}, Total: {estado['total']}, Estado: {estado['estado']}\n"
            elif msj == "salir":
                rta = "¡Hasta luego!\n"
                break
            else:
                rta = "Comando no reconocido. Usá 'pedir', 'ver_mano' o 'salir'.\n"

            conection.sendall(rta.encode())
        except:
            break

    print(f"[-] Cliente {address} desconectado")
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
