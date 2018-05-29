from collections import namedtuple
import doctest
import datetime
import unittest
import pytest

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
    ('Иванов Иван', 225000)
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


@pytest.mark.parametrize('data, expected', [('Ромашкин    Филимон 20          1000', ('Ромашкин Филимон', 20000)),
                                            ('Иванов      Иван    45          5000', ('Иванов Иван', 225000))])
def test_fio(data, expected):
    assert salary_calc(data) == expected, 'Неверный ФИО'


def test_salary():
    assert salary_calc('Ромашкин    Филимон 20          1000')[1] == 20000, 'Неверная сумма'
# ************************assertion tests end ****************************************

# class can be tested by doctest


class Employee:
    """class Employee
    >>> e = Employee('Ромашкин Филимон', 1990)
    >>> e.age
    28
    >>> print(e)    # doctest: +NORMALIZE_WHITESPACE
    Ромашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин ФилимонРомашкин Филимон
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
        self.assertEqual(salary_calc('Ромашкин    Филимон 20          1000')[1], 20000, "Неверная сумма")

    def test_salary_fio(self):
        self.assertIn('Ромашкин Филимон',salary_calc('Ромашкин    Филимон 20          1000'), "Неверное ФИО")

    def test_salary_exception(self):
        with self.assertRaises(ValueError):
            salary_calc('x x x x')

# print(salary_calc('Ромашкин    Филимон 20          1000'))
# print(salary_calc('Иванов      Иван    45          5000'))

# assert raises exception AssertionError
# salary_calc('')
# assert salary_calc('Ромашкин    Филимон 20          1000')[1] == 21000, 'Неверная сумма'

if __name__ == '__main__':
    test_empty_str()
    test_salary()
    # tests all >>> expressions in function documentation
    doctest.testmod()
    unittest.main()
