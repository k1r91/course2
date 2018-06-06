import socketserver

from db import DB
from transaction import Transaction, ServiceTransaction, PaymentTransaction, EncashmentTransaction


class PaymentServer(socketserver.BaseRequestHandler):

    host = 'localhost'
    port = 9999
    db = DB()

    def handle(self):

        self.data = self.request.recv(1024)
        tr_type = Transaction.get_type(self.data)
        tr = None
        if tr_type == 1:    # process payment transaction
            tr = PaymentTransaction.deserialize(self.data)
            self.request.sendall(bytes('200', 'utf-8'))
        elif tr_type == 2:  # process encashment transaction
            tr = EncashmentTransaction.deserialize(self.data)
            self.request.sendall(bytes('200', 'utf-8'))
        elif tr_type == 0:  # Process service transaction
            tr = ServiceTransaction.deserialize(self.data)
            if tr.action == 0:  # terminal power on
                # check terminal for registration in our database
                if self.check_terminal_registration(tr):
                    self.request.sendall(bytes('200', 'utf-8'))
                else:
                    self.request.sendall(bytes('401', 'utf-8'))
            elif tr.action == 2:    # terminal shutdown
                self.write_terminal_config(tr)
        self.save_transaction(tr)
        print('Client {} says: {}'.format(self.client_address[0], self.data))
        print('Deserialized data: {}'.format(tr))

    @staticmethod
    def serve():
        print('Payment server started')
        server = socketserver.TCPServer((PaymentServer.host, PaymentServer.port), PaymentServer)
        server.serve_forever()

    def write_terminal_config(self, tr):
        query = '''UPDATE terminal SET last_transaction_id = ?, cash = ? , state = ? WHERE id = ?'''
        self.db.cursor.execute(query, (tr.tr_id, tr.cash, tr.state, tr.term_id))
        self.db.conn.commit()

    def check_terminal_registration(self, tr):
        query = '''SELECT * FROM terminal WHERE id = ?'''
        result = self.db.cursor.execute(query, (tr.term_id,))
        if result.fetchall():
            return True
        return False

    def save_transaction(self, tr):
        base_query = 'INSERT INTO {} (length, term_id, transaction_id, datetime, type, '.format(
            Transaction.__tablename__)
        if tr.TYPE == 0:        # saving service transaction
            query = base_query + 'action) VALUES (?, ?, ?, ?, ?, ?)'
            self.db.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.action))
            self.db.conn.commit()
        elif tr.TYPE == 1:      # saving payment transaction
            query = base_query + 'org_id, amount) VALUES (?, ?, ?, ?, ?, ?, ?)'
            self.db.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.org_id, tr.amount))
            self.db.conn.commit()
        elif tr.TYPE == 2:      # saving encashment transaction
            query = base_query + 'collector_id, amount) VALUES (?, ?, ?, ?, ?, ?, ?)'
            self.db.cursor.execute(query, (tr.length, tr.term_id, tr.tr_id, tr.date, tr.TYPE, tr.collector_id,
                                           tr.amount))
            self.db.conn.commit()


if __name__ == '__main__':
    PaymentServer.serve()