import socket
import random
from transaction import ServiceTransaction, PaymentTransaction, EncashmentTransaction


class Terminal:

    host = 'localhost'
    port = 9999

    def __init__(self, id):
        self.id = id

    def send(self, data):
        if not isinstance(data, bytes):
            data = bytes(data, 'utf-8')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.sendall(data)
        result = str(self.sock.recv(1024), 'utf-8')
        self.sock.close()
        return result

    @staticmethod
    def create_rnd_transaction():
        tr_class = random.choice([ServiceTransaction, PaymentTransaction, EncashmentTransaction])
        transaction = None
        if tr_class.__name__ == 'ServiceTransaction':
            action = random.choice(['power_on', 'reload', 'shutdown', 'activate_sensor', 'block'])
            transaction = tr_class(action)
        elif tr_class.__name__ in ['PaymentTransaction', 'EncashmentTransaction']:
            transaction = tr_class(random.randint(0, 1000), random.randint(50, 50000))
        return transaction

if __name__ == '__main__':
    t1 = Terminal(500)
    print(t1.send('test'))
    Terminal.create_rnd_transaction()