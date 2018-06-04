# common context manager
class ListTransaction:

    def __init__(self, thelist):
        self.thelist = thelist

    def __enter__(self):
        self.workingcopy = list(self.thelist)
        return self.workingcopy

    def __exit__(self, exc_type, value, traceback):
        print(dir(traceback))
        print("Exception type: {}, value: {}, traceback: {}".format(exc_type, value, traceback))
        if exc_type is None:
            self.thelist[:] = self.workingcopy
        return False

items = [1, 2, 3]

try:
    with ListTransaction(items) as working:
        working.append(5)
        working.append(6)
        working[10] = 25
except IndexError:
    pass
print(items)