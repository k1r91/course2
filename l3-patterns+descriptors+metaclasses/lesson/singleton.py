class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class A():
    pass


class B(metaclass=Singleton):
    pass

e = A()
d = A()
c = B()
d = B()
print(e is d)
print(c is d)