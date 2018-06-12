from abc import ABCMeta, abstractmethod, abstractproperty


class Foo(metaclass=ABCMeta):

    @abstractmethod
    def spam(self, a, b):
        pass

    @property
    @abstractmethod
    def name(self, asd):
        pass


class Grok:
    pass

Foo.register(Grok)

g = Grok()
print(isinstance(g, Foo))