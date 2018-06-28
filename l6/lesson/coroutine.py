from collections import deque


def countdown(n):
    while n > 0:
        print('Loosing resources ...', n)
        yield
        n -= 1
    print('bankrupt')


def countup(n):
    x = 0
    while x < n:
        print('Profit grows', x)
        yield
        x += 1


class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        self._task_queue.append(task)

    def run(self):
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                print('Task {} completed'.format(task))

scheduler = TaskScheduler()
scheduler.new_task(countup(12))
scheduler.new_task((countdown(10)))
scheduler.run()