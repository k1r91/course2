import sys
import unittest
import pytest
sys.path.append('..')
from transaction import Transaction, SerializeException, ServiceTransaction, EncashmentTransaction, PaymentTransaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.t = Transaction(50, 50)
        self.st = ServiceTransaction(50, 2, 'reload', {'last_transaction_id': 25,'cash': 5000, 'state': 1})
        self.pt = PaymentTransaction(50, 1, 225, 89049864438, 11000, 1)
        self.et = EncashmentTransaction(50, 4, 567, 20000)

    def test_common_transaction_length(self):
        self.assertEqual(self.t.get_length(), 17)

    def test_check_header(self):
        self.assertEqual(Transaction.check_header(0x7a7a), True)

    def test_get_datetime(self):
        self.assertIsInstance(Transaction.get_datetime(), tuple, 'Return value is not tuple.')

    def test_fmt_size(self):
        self.assertIsInstance(Transaction.fmt_size(), int)

    def test_seconds_since_midnight(self):
        self.assertIsInstance(Transaction.seconds_since_midnight(), int, 'Return value is not integer')

    def test_servicetransaction_serialize(self):
        self.assertIsInstance(self.st.serialize(), bytes)


@pytest.mark.parametrize('total_seconds, expected', [(86399, (23, 59, 59)),
                                                     (7825, (2, 10, 25)),
                                                     (43200, (12, 0, 0))])
def test_transaction_get_time(total_seconds, expected):
    assert Transaction.get_time(total_seconds) == expected, 'Incorrect get_time function behaviour'


@pytest.mark.parametrize('dict_data, value, expected', [({6: 'asd', 100: '32'}, 'asd', 6),
                                                        ({100: 25, 400: 46}, 25, 100),
                                                        ({'asd': 'fgh', 5: 'asd'}, 'fgh', 'asd')])
def test_servicetransaction_get_key(dict_data, value,  expected):
    assert ServiceTransaction.get_key(dict_data, value) == expected, 'Wrong key of dictionary'
