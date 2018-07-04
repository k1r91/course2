
def gen():
    yield 'Hello'
    while True:
        x = yield
        print('Hello' * x)

g = gen()
print(next(g))
print(next(g))
g.send(10)
g.send(15)
try:
    print(next(g))
except TypeError as e:
    print(e)


def splitter(s):
    while True:
        string = yield
        yield string.split(s)

spl = splitter(',')
next(spl)
print(spl.send('a, b, c, d, e'))
next(spl)
print(spl.send('a, b, c, d, f'))