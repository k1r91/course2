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
            self.config = json.load(config_file)
            print(self.config)
            self._id = self.config['id']
            self.title = self.config['title']
            self.cash = self.config['cash']
            self.last_transaction_id = self.config['last_transaction_id'] + 1
            self.state = self.config['state']
            if self.power_on() == '401':
                raise ValueError("Terminal is not registered in database.")

    def send(self, data):
        self.last_transaction_id += 1
        self.config['last_transaction_id'] = self.last_transaction_id
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(data)
        result = str(sock.recv(1024), 'utf-8')
        sock.close()
        return result

    def power_on(self):
        tr = ServiceTransaction(self._id, self.last_transaction_id, 'power_on', self.config)
        result = self.send(tr.serialize())
        return result

    def power_off(self):
        tr = ServiceTransaction(self._id, self.last_transaction_id, 'shutdown', self.config)
        result = self.send(tr.serialize())
        return result

    def create_rnd_transaction(self):
        tr_class = random.choice([PaymentTransaction, EncashmentTransaction])
        transaction = tr_class(self._id, self.last_transaction_id, random.randint(0, 65000),
                                   random.randint(1000, 10000000))
        return transaction

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        with open(self.config_file, 'w') as config_file:
            self.power_off()
            self.config['title'] = self.title
            self.config['last_transaction_id'] = self.last_transaction_id - 1
            self.config['cash'] = self.cash
            self.config['state'] = self.state
            json.dump(self.config, config_file)
        return False

    def __str__(self):
        return '{}: id={}, last_transaction_id={}, configuartion_file={}, cash={}'.format(self.title,
                                                                                          self._id,
                                                                                          self.last_transaction_id,
                                                                                          self.config_file,
                                                                                          self.cash)

if __name__ == '__main__':
    with Terminal(1049) as terminal1:
        print(terminal1)
        tr = terminal1.create_rnd_transaction()
        terminal1.send(tr.serialize())