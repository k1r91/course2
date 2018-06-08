class A:
    __slots__ = ['name']
    pass

a = A()
a.name = 22
try:
    print(a.__dict__)
except AttributeError:
    print("{} has no __dict__".format(a.__class__.__name__))

try:
    a.x = 123
except AttributeError:
    print("Cannot set x because of __slots__")