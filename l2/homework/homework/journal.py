class MetaList(type):
    def __call__(cls, *args, **kwargs):
        setattr(cls, cls.__name__, list())
        setattr(cls, 'id', '0000000000000')
        return cls


class Journal(metaclass=MetaList):
    pass

if __name__ == '__main__':
    t = Journal()
    print(t)
    print(dir(t))
    print(t.Journal)
