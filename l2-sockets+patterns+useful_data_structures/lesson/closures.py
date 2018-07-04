

def callf(func):
    return func()


def bar():
    x = 13


def helloworld():
    return 'Hello world!'


print(callf(helloworld))
