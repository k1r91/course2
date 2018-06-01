import socketserver

from transaction import Transaction, ServiceTransaction, PaymentTransaction, EncashmentTransaction


class PaymentServer(socketserver.BaseRequestHandler):

    host = 'localhost'
    port = 9999

    def handle(self):
        self.data = self.request.recv(1024).decode()
        tr_type = Transaction().get_type(self.data)
        if tr_type == 1:    # Payment transaction
            tr = PaymentTransaction.deserialize(self.data)
        elif tr_type == 2:  # Process to encashment transaction
            tr = EncashmentTransaction.deserialize(self.data)
        elif tr_type == 0:  # Process to Service transaction
            tr = ServiceTransaction.deserialize(self.data)
        print('Client {} says: {}'.format(self.client_address[0], self.data))
        print('Deserialized data: {}'.format(tr))
        self.request.sendall(bytes('Message received', 'utf-8'))

    @staticmethod
    def serve():
        print('Payment server started')
        server = socketserver.TCPServer((PaymentServer.host, PaymentServer.port), PaymentServer)
        server.serve_forever()


if __name__ == '__main__':
    PaymentServer.serve()