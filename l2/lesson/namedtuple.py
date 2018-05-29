from collections import namedtuple
Person = namedtuple('Person', ('name', 'age'))
chel = Person('Rostislav', 27)
print(chel.name)
chel.name = 'Pavel'
print(chel.name)
