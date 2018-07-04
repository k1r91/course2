# Descriptors


class TypedProperty:
    def __init__(self, name, type_, default=None):
        self.name = '_' + name
        self.type = type_
        self.default = default if default else type_()
        pass

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('Value type must be {}'.format(self.type))
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError('Cannot delete attribute')


class Example:
    name = TypedProperty('name', str)
    num = TypedProperty('num', int, 'num!')

ex = Example()
print(ex.num)
ex.name = 'asd'
print(ex.name, ex.num)
try:
    ex.name = 25
except TypeError:
    print('boroda')
del ex.name
print(ex.name)