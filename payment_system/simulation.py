import random
import time
from terminal import Terminal

if __name__ == '__main__':
    terminals = [Terminal(248), Terminal(582), Terminal(645), Terminal(997), Terminal(255)]
    while True:
        term = random.choice(terminals)
        time.sleep(.5)
        transaction = term.create_rnd_transaction()
        received = term.send(transaction.serialize())
        print(received)