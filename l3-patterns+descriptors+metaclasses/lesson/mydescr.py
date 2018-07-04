class TypedProperty:
    def __init__(self, name, _type, default=None):
        self.name = '_' + name
        self.type = _type
        self.default = default if default else _type()
        # self.__set__(self, default)

    def __get__(self, instance, owner):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Type must me {}".format(self.type))
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Cannot delete typed property")

class Example:
    name = TypedProperty('name', str, 'bugaga')

ex = Example()
print(ex.name)
del ex.name