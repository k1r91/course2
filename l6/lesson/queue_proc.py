import multiprocessing as mp
import time
from collections import Counter
from random import choice, randint

from app_log import get_logger


def gnome(out_q, treasure):
    logger = get_logger('queue', 'queue_proc.log')
    while True:
        for i in range(randint(1, 10)):
            data = choice(treasure)
            out_q.put(data)
        logger.info('Gnome was working. Now rest...')
        time.sleep(.1)


def gnome_king(in_q):
    gnomes_cave = []
    logger = get_logger('queue', 'queue_proc.log')
    while True:
        data = in_q.get()
        if data is None:
            logger.info('King: i have to exit')
            logger.info('Queue: {}'.format(in_q.qsize()))
            break
        logger.info('The King: gnome bring me {}'.format(data))
        gnomes_cave.append(data)
    logger.info('King: gnome bring me {}'.format(Counter(gnomes_cave)))
    return gnomes_cave

if __name__ == '__main__':
    treasure = ('Gold', 'Silver', 'Diamond', 'Ruby', 'Chocolate')
    q = mp.Queue()
    p1 = mp.Process(target=gnome_king, args=(q, )) # no daemon, because putting None breaks king cycle
    p2 = mp.Process(target=gnome, args=(q, treasure), daemon=True)
    p1.start()
    p2.start()
    time.sleep(5)
    p2.terminate()
    q.put(None)
    # time.sleep(1)