import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8888))
i = 0
while True:
    i += 1
    tm = s.recv(1024)
    print('{}. Received time: {}'. format(i, tm.decode('ascii')))

s.close()