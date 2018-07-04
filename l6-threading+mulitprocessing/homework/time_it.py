import time
from functools import wraps


def time_it(func):
    def deco(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        delta = time.time() - start
        print('Function {} worked {} seconds.'.format(func.__name__, delta))
        return result
    return deco
