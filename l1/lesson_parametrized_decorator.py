import datetime
import time
from functools import wraps


def sleep(sec):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            print('Sleeping {} seconds'.format(sec))
            time.sleep(sec)
            res = func(*args, **kwargs)
            return res
        return decorated
    return decorator


def time_it(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)
        delta = time.time() - now
        print('Function {} was worked {} seconds.'.format(func.__name__, delta))
        return res
    return decorator


@time_it
@sleep(.2)
def str_add(numbers):
    res = ''
    for i in range(numbers):
        res = res + ' ' + str(i)
    return res


@time_it
@sleep(.2)
def str_join(numbers):
    res = ' '.join(list(map(str, range(numbers))))
    return res


@time_it
@sleep(.2)
def str_join_v2(numbers):
    nums = []
    for i in range(numbers):
        nums.append(str(i))
    return ' '.join(nums)

if __name__ == '__main__':
    MAX = 100000
    str_add(MAX)
    str_join(MAX)
    str_join_v2(MAX)