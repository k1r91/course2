import random
import time
from terminal import Terminal

if __name__ == '__main__':
    with Terminal(7) as t7, Terminal(55) as t55, Terminal(250) as t250, Terminal(304) as t304, Terminal(1049) as t1049:
        while True:
            term = random.choice([t7, t55, t250, t304, t1049])
            time.sleep(.5)
            term.send_random_transaction()
