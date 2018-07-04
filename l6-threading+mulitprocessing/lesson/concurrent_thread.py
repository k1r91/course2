import threading
import time
from collections import deque
from random import randint

from lesson.app_log import get_logger

flag = threading.Condition()

q = deque()
logger = get_logger('condition', 'th_cond.log')


def producer():
    i = 0
    while True:
        flag.acquire()
        while len(q) < 100:
            logger.info('Ice cream producer. To little ice cream ({}). Procude!'.format(len(q)))
            q.append('Ice cream - {}'.format(i))
            i += 1
        flag.notify()
        flag.release()
        logger.info('Now in truck: {}'.format(len(q)))


def consumer():
    while True:
        logger.info('Consumer. Waiting for ice cream ...' )
        flag.acquire()

        while not q:
            flag.wait()
        logger.info('Consumer. Now eating ...')
        for i in range(randint(1, 100)):
            logger.info('Consumer. Eat ice cream!')
            good = q.popleft()

        flag.release()
        time.sleep(2)

pt = threading.Thread(target=producer)
ct = threading.Thread(target=consumer)
print('Starting producer and consumer')
pt.start()
# time.sleep(1)
ct.start()
time.sleep(5)
print('Time expired')