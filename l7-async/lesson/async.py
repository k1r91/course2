import time
import asyncio

# Promise

# Future / Task

# zeroMQ - azmq

# uvloop (libuv) (Unix)

async def _task(name, sec):
    print('Task {} was started'.format(name))
    try:
        await asyncio.sleep(sec)
    except asyncio.CancelledError:
        print('I was killed')
    print('Task {} was finished'.format(name))
    return 'Task {} was finished'.format(name)

async def manager():
    # task1 = asyncio.ensure_future(_task('task1', 7))
    # task2 = asyncio.ensure_future(_task('task2', 5))
    await asyncio.wait([_task('task1', 7), _task('task2', 5)])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        print('Start event loop')
        # loop.run_until_complete(task1)    # Consistent exectution
        loop.run_until_complete(manager())
    finally:
        loop.close()

