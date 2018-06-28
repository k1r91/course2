import socketserver

from paymentserver import PaymentServerHandler


class PaymentServerSingleThread(PaymentServerHandler):


    @staticmethod
    def serve():
        print('Payment server started')
        server = socketserver.TCPServer((PaymentServerHandler.host, PaymentServerHandler.port), PaymentServerHandler)
        server.serve_forever()

if __name__ == '__main__':
    with PaymentServerSingleThread.serve():
        pass
