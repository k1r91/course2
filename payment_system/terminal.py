import os
import socket
import random
import json
import db
import hashlib
from transaction import ServiceTransaction, PaymentTransaction, EncashmentTransaction, PaymentTransactionException, \
    EncashmentTransactionException


class TerminalException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


class Terminal:

    host = 'localhost'
    port = 9999
    config_folder = 'terminals'

    def __init__(self, _id):
        self.config_file = os.path.join(self.config_folder, str(_id), ''.join([str(_id), '.json']))
        with open(self.config_file, 'r') as config_file:
            self.config = json.load(config_file)
            self.state = self.config['state']
            self.check_block()
            self._id = self.config['id']
            self.title = self.config['title']
            self.cash = self.config['cash']
            self.last_transaction_id = self.config['last_transaction_id'] + 1
        self.power_on()
        self.incorrect_code = 0
        self.db_org = db.DatabaseOrganization()
        self.db_org_cursor = self.db_org.conn.cursor()

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
        self.config['last_transaction_id'] += 1
        tr = ServiceTransaction(self._id, self.last_transaction_id, 'power_on', self.config)
        response = self.send(tr.serialize())
        if response != '200':
            raise TerminalException('Error {}'.format(response))
        return True

    def create_rnd_transaction(self):
        self.check_block()
        transaction = None
        tr_class = random.choice([PaymentTransaction, EncashmentTransaction])
        if tr_class.__name__ == 'PaymentTransaction':
            transaction = tr_class(self._id, self.last_transaction_id, random.randint(0, 65000),
                                   random.randint(1000, 10000000), random.randint(1000, 10000000))
        elif tr_class.__name__ == 'EncashmentTransaction':
            transaction = tr_class(self._id, self.last_transaction_id, random.randint(0, 65000),
                                   random.randint(1000, 10000000))
        return transaction

    def send_payment_transaction(self, org_id, p_acc, amount):
        self.check_block()
        query = "SELECT * FROM organization WHERE id = ?"
        result = self.db_org_cursor.execute(query, (org_id, )).fetchall()
        if not result:
            raise PaymentTransactionException('Error 402')
        commission = result[0][2]
        tr = PaymentTransaction(self._id, self.last_transaction_id, org_id, p_acc, amount, commission)
        response = self.send(tr.serialize())
        if response == '200':
            self.cash += amount
            self.save_config()
        else:
            raise PaymentTransactionException("Error {}".format(response))

    def send_encashment_transaction(self, collector_id, amount, secret):
        self.check_block()
        query = "SELECT * FROM collector WHERE id = ?"
        result = self.db_org_cursor.execute(query, (collector_id, )).fetchall()
        if not result or hashlib.sha256(secret.encode('utf-8')).hexdigest() != result[0][4]:
            self.incorrect_code += 1
            if self.incorrect_code == 3:
                self.state = 0
                raise TerminalException('Error 408')
            raise EncashmentTransactionException('Error 406')
        if amount > self.cash:
            raise EncashmentTransactionException('Error 407')
        tr = EncashmentTransaction(self._id, self.last_transaction_id, collector_id, amount)
        response = self.send(tr.serialize())
        print(response)
        if response == '200':
            self.cash -= amount
            self.save_config()
        else:
            raise EncashmentTransactionException("Error {}".format(response))

    def save_config(self):
        with open(self.config_file, 'w') as config_file:
            self.config['title'] = self.title
            self.config['last_transaction_id'] = self.last_transaction_id - 1
            self.config['cash'] = self.cash
            self.config['state'] = self.state
            json.dump(self.config, config_file)

    def save_config_to_db(self):
        tr = ServiceTransaction(self._id, self.last_transaction_id, 'shutdown', self.config)
        result = self.send(tr.serialize())
        return result

    def check_block(self):
        if not self.state:
            raise TerminalException('Error 408')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        self.save_config_to_db()
        self.save_config()
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
        terminal1.send_payment_transaction(25, 3249234, 1000)
        try:
            terminal1.send_encashment_transaction(488, 10, 'dncornho7757411')
        except EncashmentTransactionException as e:
            print(e.msg)
        try:
            terminal1.send_encashment_transaction(488, 10, 'dncornho7757411')
        except EncashmentTransactionException as e:
            print(e.msg)
        try:
            terminal1.send_encashment_transaction(488, 1000, 'dncornho775741')
        except EncashmentTransactionException as e:
            print(e.msg)