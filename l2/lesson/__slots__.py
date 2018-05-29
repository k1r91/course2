class BasicClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

bc = BasicClass(13, 42)
print(bc.__dict__)
bc.z = 777
print(bc.__dict__)


class StrictClass:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
sc = StrictClass(13, 42)
# strict classes has no dict attribute
# print(sc.__dict__)
sc.x = 25   # it's ok
try:
    sc.z = 16
except AttributeError:
    print("You cannot set attributes to strict classes, because this attributes not in __slots__")

print(sc.__sizeof__(), bc.__sizeof__())