import threading
import time

class Task:

    def __init__(self):
        self.running = True

    def start(self):
        t = threading.Thread(target=self.run)
        t.start()

    def run(self):
        while self.running:
            print('*', end='')

    def stop(self):
        self.running = False

t = Task()
t.start()
time.sleep(2)
t.stop()