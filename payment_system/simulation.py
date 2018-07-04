import threading
import multiprocessing
import time
import random
from queue import Queue
from terminal import Terminal
import sys


def simulate(q):
    with Terminal(1049) as t1049, Terminal(7) as t7, Terminal(250) as t250, Terminal(55) as t55, Terminal(304) as t304:
        tlist = [t7, t55, t250, t304, t1049]
        while not q.empty():
            term = random.choice(tlist)
            time.sleep(.5)
            term.simulate_action()

if __name__ == '__main__':
    q = Queue()
    q.put(True)
    task = threading.Thread(target=simulate, args=(q, ))
    task.start()
    input('Press ENTER to stop simulation')
    q.get()