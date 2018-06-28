import socketserver
import threading

from paymentserver import PaymentServerHandler


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999
    server = ThreadedTCPServer((HOST, PORT), PaymentServerHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        print('Threading payment server started')
        server_thread.start()
