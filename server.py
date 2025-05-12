import socket
import threading
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
    conection.sendall("Bienvenido al servidor de Blackjack.\nIngrese su nombre:\n".encode())
    nombre = conection.recv(1024).decode().strip()
    jugador = Player(nombre)

    conection.sendall("Comandos:\n[VER_MESAS]\n[CREAR_MESA]\n[UNIRSE_MESA <id>]\n".encode())

    mesa_asignada = None

    while not mesa_asignada:
        try:
            data = conection.recv(1024).decode().strip()
            if data == "VER_MESAS":
                if not mesas:
                    conection.sendall("No hay mesas disponibles.\n".encode())
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
                        conection.sendall("ID de mesa inválido.\n".encode())
                except:
                    conection.sendall("Uso incorrecto. Ej: UNIRSE_MESA 1\n".encode())
            else:
                conection.sendall("Comando no reconocido.\n".encode())
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
            estado = mesa_asignada.get_estado_de(conection)

            if msj == "pedir":
                if estado["estado"] != "jugando":
                    rta = f"No podés pedir más cartas. Estado actual: {estado['estado']}.\n"
                else:
                    carta = mesa_asignada.repartir_a(conection)
                    estado = mesa_asignada.get_estado_de(conection)
                    rta = f"Carta: {carta}, Total: {estado['total']}, Estado: {estado['estado']}\n"

            elif msj == "stand":
                if estado["estado"] != "jugando":
                    rta = f"Ya estás en estado: {estado['estado']}.\n"
                else:
                    mesa_asignada.plantarse(conection)
                    estado = mesa_asignada.get_estado_de(conection)
                    rta = f"Te has plantado con un total de {estado['total']}.\n"

            elif msj == "ver_mano":
                rta = f"Mano: {estado['mano']}, Total: {estado['total']}, Estado: {estado['estado']}\n"

            elif msj == "salir":
                rta = "¡Hasta luego!\n"
                break

            else:
                rta = "Comando no reconocido. Usá: pedir, stand, ver_mano o salir.\n"

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
