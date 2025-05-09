import socket
import threading

HOST = '0.0.0.0'
PORT = 22223

def manejo_cliente(conection, address):
    print(f"Conexión establecida con {address}")
    conection.sendall(b"Conectado al servidor\n")
    while True:
        try:
            data= conection.recv(1024)
            if not data:
                break
            print(f"[{address}] -> {data.decode().strip()}")
            conection.sendall(b"Recibido\n")

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