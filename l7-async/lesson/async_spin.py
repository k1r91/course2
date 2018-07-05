import asyncio
import itertools
import time
import sys

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break

    write(' ' * len(status) + '\x08' * len(status))


def process_bar(x=1):
    print('#', end='')
    percent = 0
    while percent < 100:
        percent = yield
        x = 80 * percent // 100
        for i in range(x):
            print('#')


async def slowpoke():
    await asyncio.sleep(5)
    return 42


async def supervisor():
    spinner = asyncio.ensure_future(spin('thinking!'))
    print('Spinner object: ', spinner)
    result = await slowpoke()
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(supervisor())
    finally:
        loop.close()
    print('Answer: ', result)

if __name__ == '__main__':
    main()