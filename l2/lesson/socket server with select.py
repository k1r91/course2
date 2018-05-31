import time
import select
import socket


def new_listen_socket(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    sock.settimeout(.2)
    return sock


def mainloop():
    address = ('', 8888)
    clients = []
    sock = new_listen_socket(address)
    while True:
        try:
            conn, addr = sock.accept()
        except OSError as e:
            pass
        else:
            print('Received connection request from {}'.format(str(addr)))
            clients.append(conn)
        finally:
            w = []
            try:
                r, w, e = select.select([], clients, [], 0)
            except Exception as e:
                pass
            for s_client in w:
                timestr = time.ctime(time.time()) + '\n'
                try:
                    s_client.send(timestr.encode('ascii'))
                except:
                    clients.remove(s_client)

print('Echo server started')
mainloop()