import socket
import sys

def main():
    if len(sys.argv) < 3:
        print("Uso: python client.py <IP> <PUERTO>")
        return
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    print(cliente.recv(1024).decode())

    try:
        while True:
            msj = input("> ")
            cliente.sendall(msj.encode())
            data = cliente.recv(1024)
            print("Servidor:", data.decode())
    except KeyboardInterrupt:
        print("\nSaliendo...")
    finally:
        cliente.close()
        
if __name__ == "__main__":
    main()