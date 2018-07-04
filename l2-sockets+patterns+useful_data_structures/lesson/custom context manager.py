import sys

class ListTransaction:

    def __init__(self, thelist):
        self.thelist = thelist

    def __enter__(self):
        self.workingcopy = list(self.thelist)
        return self.workingcopy

    def __exit__(self, type, value, tb):
        if type is None:
            self.thelist[:] = self.workingcopy
        return False


items = [1, 2, 3]
with ListTransaction(items) as working:
    working.append(4)
    working.append(5)
print(items)

try:
    with ListTransaction(items) as working:
        working.append(6)
        working.append(7)
        raise RuntimeError('')
except RuntimeError:
    pass
print(items)


class Mirror:

    def __enter__(self):
        """
        change standart output to reverse
        """
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'Kirill'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please do not divide on zero")
        return True

with Mirror() as enter_value:
    print('Reverse writing')
    print(enter_value)

print('Output text')
write = sys.stdout.write
def reverse(text):
    write(text[::-1])
sys.stdout.write = reverse
print('test')