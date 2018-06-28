import time
from collections import Counter
from queue import Queue
from random import choice, randint
from threading import Thread

from lesson.app_log import get_logger

gnomes_cave=[]
treasure = ('Gold', 'Silver', 'Diamonds', 'Ruby')
logger = get_logger('queue_thread', 'queue.log')


def gnome(out_q):
    while True:
        for i in range(randint(1, 10)):
            data = choice(treasure)
            out_q.put(data)
        logger.info('Gnome was working. Now rest...')
        time.sleep(.1)


def gnome_king(in_q):
    while True:
        data = in_q.get()
        logger.info('The King: gnome bring me {}'.format(data))
        gnomes_cave.append(data)

q = Queue()
t1 = Thread(target=gnome_king, args=(q, ), daemon=True)
t2 = Thread(target=gnome, args=(q, ), daemon=True)
t1.start()
t2.start()
time.sleep(5)
print(Counter(gnomes_cave))