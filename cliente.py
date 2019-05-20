import pickle
import socket
import zlib
import time

def main():
    #host = "10.10.173.250"
    HOST = "10.10.173.250"
    PORT = 6666
    print("Intentando conectar a %s" % HOST)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(b"dame lista")
        data = s.recv(2048)
        data = pickle.loads(data)
    print('Received',repr(data))

if __name__ == "__main__":
    inicio = time.time()
    main()
    duracion = time.time() - inicio
    print("tiempo de ejecución: %f" % duracion)

