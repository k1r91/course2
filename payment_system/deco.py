import time
from functools import wraps


def time_it(func):
    @wraps(func)
    def deco(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        delta = time.time() - start
        print('Function {} worked {} seconds.'.format(func.__name__, delta))
        return res
    return deco