from collections import namedtuple
import doctest
import datetime
import unittest

DATA = '''
Фамилия     Имя     Часов       Ставка
Ромашкин    Филимон 20          1000
Иванов      Иван    45          5000
'''

Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))


# doctest on function

def salary_calc(line):
    """вычисление зарплаты сотрудника

    >>> salary_calc('Ромашкин    Филимон 20          1000')
    ('Ромашкин Филимон', 20000)
    >>> salary_calc('Иванов      Иван    45          5000')
    ('Иванов Иван', 224000)
    """
    if line:
        data = Salary(*line.split())
        fio = ' '.join([data.surname, data.name])
        salary = int(data.worked) * int(data.rate)
        res = (fio, salary)
    else:
        res = ()
    return res

# ************************assertion tests ****************************************
# raises Assertion error exception every time


def test_empty_str():
    assert salary_calc('') == (), 'Непустые данные'


def test_fio():
    assert salary_calc('Ромашкин    Филимон 20          1000')[0] == 'Ромашкин Филимон', 'Неверный ФИО'


def test_salary():
    assert salary_calc('Ромашкин    Филимон 20          1000')[1] == 20000, 'Неверная сумма'
# ************************assertion tests end ****************************************

# class can be tested by doctest


class Employee:
    """class Employee
    >>> e = Employee('Ромашкин Филимон', 1990)
    >>> e.age
    27
    >>> print(e)    # doctest: +NORMALIZE_WHITESPACE
    'Ромашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин
    ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин ИванРомашкин Иван'
    """
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    @property
    def age(self):
        return datetime.date.today().year - self.birth_year

    def __str__(self):
        return self.name * 15


# unittest
class TestSalary(unittest.TestCase):
    def test_salary_summ(self):
        pass

# print(salary_calc('Ромашкин    Филимон 20          1000'))
# print(salary_calc('Иванов      Иван    45          5000'))

# assert raises exception AssertionError
# salary_calc('')
# assert salary_calc('Ромашкин    Филимон 20          1000')[1] == 21000, 'Неверная сумма'

if __name__ == '__main__':
    test_empty_str()
    test_fio()
    test_salary()
    # tests all >>> expressions in function documentation
    doctest.testmod()
