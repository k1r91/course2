import os
import socket
import struct
import time
import multiprocessing as mp

FILE_DIR = os.path.join(os.path.dirname(__file__), 'download')
HOST, PORT = 'localhost', 5555
if os.path.exists('upload/test.jpeg'):
    os.remove('upload/test.jpeg')


def upload_file(scandir_obj):
    size = os.path.getsize(scandir_obj.path)
    print(size)
    # print(scandir_obj.name, scandir_obj.path, os.path.getsize(scandir_obj.path))
    with open(scandir_obj.path, 'rb') as up_f:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        while True:
            data = up_f.read(1024)
            if not data:
                break
            sock.sendall(data)
            receive = sock.recv(1024)
            print(receive)
        sock.close()


if __name__ == '__main__':
    for file in os.scandir(FILE_DIR):
        task = mp.Process(target=upload_file, args=(file, ))
        task.run()
        break