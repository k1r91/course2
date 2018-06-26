import os
import socket
import random
import json
import threading
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
    config_folder = os.path.join(os.path.dirname(__file__), 'terminals')

    def __init__(self, _id):
        """
        reads configuration file, checks block, checks record about this terminal in database, initialize
        cursor to organizations database
        :param _id: terminal id 
        """
        self.db_org = db.DatabaseOrganization()
        self.db_org_cursor = self.db_org.conn.cursor()
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

    def send(self, data):
        """
        send data to payment server
        :param data: binary string
        :return: server response
        """
        result = []

        def thread(self, result, data=data):
            self.last_transaction_id += 1
            self.config['last_transaction_id'] = self.last_transaction_id
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.sendall(data)
            result.append(str(sock.recv(1024), 'utf-8'))
            sock.close()
        task = threading.Thread(target=thread, args=(self, result, data, ))
        task.start()
        task.join()
        try:
            return result[0]
        except IndexError:
            return '409'

    def power_on(self):
        """
        Send power_on service transaction to payment server 
        :return: True if response of server is ok (information about terminal in database)
        """
        self.config['last_transaction_id'] += 1
        tr = ServiceTransaction(self._id, self.last_transaction_id, 'power_on', self.config)
        response = self.send(tr.serialize())
        if response != '200':
            raise TerminalException('Error {}'.format(response))
        return True

    def simulate_action(self):
        """if cash is full(10000000), simulate encashment, else simulate payment transaction
        """
        self.check_block()
        if self.cash > 10000000:
            self.send_encashment_transaction(488, self.cash, 'dncornho775741')
        else:
            query = 'SELECT id FROM organization'
            result = self.db_org_cursor.execute(query)
            org_id = random.choice(result.fetchall())[0]
            amount = random.randint(PaymentTransaction.MIN_AMOUNT, PaymentTransaction.MAX_AMOUNT)
            random_acc = random.randint(1000000, 9999999)
            self.send_payment_transaction(org_id, random_acc, amount)

    def send_payment_transaction(self, org_id, p_acc, amount):
        self.check_block()
        self.db_org = db.DatabaseOrganization()
        self.db_org_cursor = self.db_org.conn.cursor()
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
        """
        state = 0 : blocked
        state = 1: unblocked
        :return: 
        """
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
        # terminal1.send_random_transaction()
        # terminal1.send_payment_transaction(25, 3249234, 1000)
        # try:
        #     terminal1.send_encashment_transaction(488, 10, 'dncornho7757411')
        # except EncashmentTransactionException as e:
        #     print(e.msg)
        # try:
        #     terminal1.send_encashment_transaction(488, 10, 'dncornho7757411')
        # except EncashmentTransactionException as e:
        #     print(e.msg)
        # try:
        #     terminal1.send_encashment_transaction(488, 1000, 'dncornho775741')
        # except EncashmentTransactionException as e:
        #     print(e.msg)