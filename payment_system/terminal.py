import socket


class Terminal:

    host = 'localhost'
    port = 9999

    def __init__(self, id):
        self.id = id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data):
        data = bytes(data, 'utf-8')
        self.sock.connect((self.host, self.port))
        self.sock.sendall(data)
        return str(self.sock.recv(1024), 'utf-8')

if __name__ == '__main__':
    t1 = Terminal(500)
    print(t1.send('test'))