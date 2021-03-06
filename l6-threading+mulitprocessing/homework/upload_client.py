import os
import socket
import struct
import multiprocessing as mp

FILE_DIR = os.path.join(os.path.dirname(__file__), 'download')
HOST, PORT = '192.168.10.123', 5555
if os.path.exists('upload/test.jpeg'):
    os.remove('upload/test.jpeg')


def upload_file(scandir_obj):
    size = os.path.getsize(scandir_obj.path)
    with open(scandir_obj.path, 'rb') as up_f:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        action = 0x06   # action for file download
        name_len = len(scandir_obj.name)
        header = struct.pack('BBQ', action, name_len, size)
        sock.sendall(header)
        sock.sendall(scandir_obj.name.encode('utf-8'))
        while True:
            data = up_f.read(1024)
            if not data:
                break
            sock.sendall(data)
            receive = sock.recv(struct.calcsize('f'))
            # print('{0:.1f}'.format(struct.unpack('f', receive)[0]))
        sock.close()


if __name__ == '__main__':
    for file in os.scandir(FILE_DIR):
        task = mp.Process(target=upload_file, args=(file, ))
        task.start()