import sys
import unittest
import pytest
sys.path.append('..')
from transaction import Transaction, SerializeException


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.t = Transaction()

    def test_length_get_time(self):
        self.assertEqual(len(self.t.get_datetime()), 40, 'Incorrect date length')

    def test_serialize_number_incorrect_year(self):
        with self.assertRaises(SerializeException):
            Transaction.serialize_number(2500, 7, is_year=True)

    def test_serialize_number_big_value(self):
        with self.assertRaises(SerializeException):
            Transaction.serialize_number(24, 4)


@pytest.mark.parametrize('number, bits, expected', [(24, 5, '11000'),
                                                        (24, 10, '0000011000'),
                                                        (86399, 24, '000000010101000101111111')])
def test_serialize_number_result(number, bits, expected):
    assert Transaction.serialize_number(number, bits) == expected, 'Incorrect output data'
