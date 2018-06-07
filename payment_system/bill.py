import os


class Bill:
    """
    My temporary bank account for processing transactions
    """

    storage = os.path.join('bill_storage', 'bill.md')

    def __init__(self):
        with open(self.storage, 'r', encoding='utf-8') as f:
            self.amount = int(f.read())

    def save(self):
        with open(self.storage, 'w', encoding='utf-8') as f:
            f.write(str(self.amount))

    def __add__(self, other):
        self.amount += other
        self.save()
        return self

    def __sub__(self, other):
        self.amount -= other
        if self.amount < 0:
            raise ValueError("You bill cannot be negative")
        self.save()
        return self

    def __str__(self):
        return "You have {} coins.".format(self.amount)


if __name__ == '__main__':
    b = Bill()
    b += 20
    b -= 30
    print(b)
