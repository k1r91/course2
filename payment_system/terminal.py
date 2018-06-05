import os
import socket
import random
import json
from transaction import ServiceTransaction, PaymentTransaction, EncashmentTransaction


class Terminal:

    host = 'localhost'
    port = 9999
    config_folder = 'terminals'

    def __init__(self, _id):
        self.config_file = os.path.join(self.config_folder, ''.join([str(_id), '.json']))
        with open(self.config_file, 'r') as config_file:
            config = json.load(config_file)
            self._id = config['id']
            self.title = config['title']
            self.cash = config['cash']
            self.last_transaction_id = config['last_transaction_id']

    def send(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(data)
        result = str(sock.recv(1024), 'utf-8')
        sock.close()
        return result

    @staticmethod
    def create_rnd_transaction():
        tr_class = random.choice([ServiceTransaction, PaymentTransaction, EncashmentTransaction])
        transaction = None
        if tr_class.__name__ == 'ServiceTransaction':
            action = random.choice(['power_on', 'reload', 'shutdown', 'activate_sensor', 'block'])
            transaction = tr_class(action)
        elif tr_class.__name__ in ['PaymentTransaction', 'EncashmentTransaction']:
            transaction = tr_class(random.randint(0, 65000), random.randint(50, 10000000))
        return transaction

    def __str__(self):
        return '{}: id={}, last_transaction_id={}, configuartion_file={}, cash={}'.format(self.title,
                                                                                          self._id,
                                                                                          self.last_transaction_id,
                                                                                          self.config_file,
                                                                                          self.cash)

if __name__ == '__main__':
    t1 = Terminal(1049)
    print(t1)
    t = Terminal.create_rnd_transaction()
    t1.send(t.serialize())