import time
import threading


def clock(interval):
    while True:
        print('Time: {}'.format(time.ctime()))
        time.sleep(interval)

t = threading.Thread(target=clock, args=(15, ))
# t.daemon = True
t.start()