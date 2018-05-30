import sys
from functools import wraps


def log(func):
    # @wraps(func)
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        print('{}({}, {}) = {}'.format(func.__name__, args, kwargs, res))
        return res
    return decorated


@log
def mul(a, b):
    return a * b

print(mul(5, 7))


class A(object):
    pass

    @log
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def __str__(self):
        return "Class A, id = {}".format(id(self))

    def __repr__(self):
        return self.__str__()

a = A()
a.x = 25

b = A()
b.x = 25

s = '001010110'
print(type(s), sys.getsizeof(s))
sbytes = bytes(s, 'utf-8')
print(type(sbytes), sys.getsizeof(sbytes))
sbytes2 = s.encode('utf-8')
print(type(sbytes2), sys.getsizeof(sbytes2), id(sbytes), id(sbytes2))
print(sbytes == sbytes2)
print(type(s), sys.getsizeof(s))
print(sys.platform)
