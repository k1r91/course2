import time
import socket
from multiprocessing import Process

HOST, PORT = 'localhost', 8888


def run(to, name):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(name.encode('utf-8'))
        data = sock.recv(1024)
        print(data)
        sock.close()
        time.sleep(to)

if __name__ == '__main__':
    p1 = Process(target=run, args=(0, 'client_1'), daemon=True)
    p1.start()
    p2 = Process(target=run, args=(0, 'client_2'), daemon=True)
    p2.start()
    p3 = Process(target=run, args=(0, 'client_3'), daemon=True)
    p3.start()
    p4 = Process(target=run, args=(0, 'client_4'), daemon=True)
    p4.start()

    time.sleep(7)