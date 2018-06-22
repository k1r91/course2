import socketserver
import socket
import threading

from db import DB, DatabaseOrganization
from transaction import Transaction, ServiceTransaction, PaymentTransaction, EncashmentTransaction
from bill import Bill


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):

        self.db_trans = DB()
        self.db_org = DatabaseOrganization()

        self.bill = Bill()
        self.data = self.request.recv(1024)
        tr_type = Transaction.get_type(self.data)
        tr = None
        errors = []

        # ***** process payment transaction *****

        if tr_type == 1:
            tr = PaymentTransaction.deserialize(self.data)
            if not self.check_valid_organization(tr.org_id):     # if organization id not in database
                self.request.sendall(bytes('402', 'utf-8'))
                return False
            if self.send_pay(tr.org_id, tr.p_acc, tr.amount, tr.commission):
                self.request.sendall(bytes('200', 'utf-8'))
            else:
                self.request.sendall(bytes('404', 'utf-8'))
                errors.append(404)

        # **** process encashment transaction *****

        elif tr_type == 2:
            tr = EncashmentTransaction.deserialize(self.data)
            if self.check_collector_requisites(tr.collector_id):
                self.bill += tr.amount
                self.request.sendall(bytes('200', 'utf-8'))
            else:
                self.request.sendall(bytes('406', 'utf-8'))
                errors.append('406')

        # **** process service transaction *****

        elif tr_type == 0:
            tr = ServiceTransaction.deserialize(self.data)
            if tr.action == 0:  # terminal power on
                # check terminal for registration in our database
                if self.check_terminal_registration(tr):
                    self.request.sendall(bytes('200', 'utf-8'))
                else:
                    self.request.sendall(bytes('401', 'utf-8'))
                    errors.append('401')
            elif tr.action == 2:    # terminal save config action (shutdown)
                self.write_terminal_config(tr)
        # save transaction in database if no errors occurred
        if not errors:
            self.save_transaction(tr)
        # TODO: log file instead of this
        print('Client {} says: {}'.format(self.client_address[0], self.data))
        print('Deserialized data: {}'.format(tr))

    @staticmethod
    def serve():
        print('Payment server started')
        server = socketserver.TCPServer((PaymentServer.host, PaymentServer.port), PaymentServer)
        server.serve_forever()

    def write_terminal_config(self, tr):
        query = '''UPDATE terminal SET last_transaction_id = ?, cash = ? , state = ? WHERE id = ?'''
        self.db_trans.cursor.execute(query, (tr.tr_id, tr.cash, tr.state, tr.term_id))
        self.db_trans.conn.commit()

    def check_terminal_registration(self, tr):
        query = '''SELECT * FROM terminal WHERE id = ?'''
        result = self.db_trans.cursor.execute(query, (tr.term_id,))
        if result.fetchall():
            return True
        return False

    def check_collector_requisites(self, col_id):
        query = '''SELECT * FROM collector WHERE id = ?'''
        result = self.db_org.cursor.execute(query, (col_id, ))
        if not result:
            return False
        return True

    def check_valid_organization(self, org_id):
        """
        :param org_id:  organization id
        :return: True if organization exists in database
        """
        query = '''SELECT * FROM organization WHERE id = ?'''
        result = self.db_org.cursor.execute(query, (org_id, )).fetchall()
        if not result:
            return False
        return True

    def save_transaction(self, tr):
        base_query = 'INSERT INTO ps_transaction (length, term_id, transaction_id, datetime, type, '
        if tr.TYPE == 0:        # saving service transaction
            query = base_query + 'action) VALUES (?, ?, ?, ?, ?, ?)'
            self.db_trans.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.action))
            self.db_trans.conn.commit()
        elif tr.TYPE == 1:      # saving payment transaction
            query = base_query + 'org_id, account, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            self.db_trans.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.org_id, tr.p_acc,
                                           tr.amount))
            self.db_trans.conn.commit()
        elif tr.TYPE == 2:      # saving encashment transaction
            query = base_query + 'collector_id, amount) VALUES (?, ?, ?, ?, ?, ?, ?)'
            self.db_trans.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.collector_id,
                                           tr.amount))
            self.db_trans.conn.commit()

    def send_pay(self, org_id, p_acc, amount, commission):
        """
        stub for sending payment for other organizations
        :param org_id: organization id
        :param p_acc: personal account
        :return:
        """
        try:
            self.bill -= amount * (1 - commission/100)
            # here we send money to other organizations (not implemented due to simplicity)
        except ValueError:
            return False
        return True


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        print('Threading payment server started')
        server_thread.start()
