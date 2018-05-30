class NoPass(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError('You can not create objects of this class')


class Cosmos(metaclass=NoPass):
    @staticmethod
    def simple():
        print('This is just Cosmos')


Cosmos.simple()
print(type(type))
print(dir(type))
print(dir(object))


# Singleton


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class Space(metaclass=Singleton):
    def __init__(self):
        print('I\'m singleton.')
a1 = Space()
b1 = Space()
print(id(a1), id(b1))

space = Cosmos()