class DocMeta(type):
    def __init__(cls, cls_name, bases, cls_dict):
        print(cls_dict.items())
        for key, value in cls_dict.items():
            if key.startswith('__'):
                continue
            if not hasattr(value, '__call__'):
                continue
            if not getattr(value, '__doc__'):
                raise TypeError("{} must have a docstring".format(key))
        type.__init__(cls, cls_name, bases, cls_dict)


# if doc is not defined, raise TypeError

class Documented(metaclass=DocMeta):

    def test(self):
        """test"""
        pass
    pass


class Foo(Documented):

    def spam(self):
        """spam"""
        pass

    def boo(self):
        pass


c = Foo()