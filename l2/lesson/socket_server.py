import os
import time
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen(5)
while True:
    client, addr = s.accept()
    print('Connection request received from {}'.format(str(addr)))
    timestr = time.ctime(time.time()) + os.linesep
    client.send(timestr.encode('utf-8'))
    client.close()