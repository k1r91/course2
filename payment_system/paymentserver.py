import socketserver

from transaction import Transaction


class PaymentServer(socketserver.BaseRequestHandler):

    host = 'localhost'
    port = 9999

    def handle(self):
        self.data = self.request.recv(1024).decode()
        print('Client {} says: {}'.format(self.client_address[0], self.data))
        self.request.sendall(bytes('Message received', 'utf-8'))

    @staticmethod
    def serve():
        print('Payment server started')
        server = socketserver.TCPServer((PaymentServer.host, PaymentServer.port), PaymentServer)
        server.serve_forever()


if __name__ == '__main__':
    PaymentServer.serve()