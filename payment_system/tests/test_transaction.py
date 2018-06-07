import sys
import unittest
import pytest
sys.path.append('..')
from transaction import Transaction, SerializeException, ServiceTransaction, EncashmentTransaction, PaymentTransaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.t = Transaction(50, 50)
        self.st = ServiceTransaction(50, 50, 'reload')
        self.pt = PaymentTransaction(50, 50, 500, 500)
        self.et = EncashmentTransaction(50, 50, 500, 500)

    def test_deserialized_type(self):
        self.assertEqual(type(self.t.deserialize(
            b'zz!\x002\x00\x00\x00\x04\x00\x00\x00\x12\x06\x05\x00\x94\xd2\x00\x00\x02')), dict)

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

    def test_servicetransaction_deserialize(self):
        st = ServiceTransaction.deserialize(b'zz\x12\x002\x00\x00\x00\x03\x00\x00\x00\x12\x06\x05\x00`\xe5\x00\x00\x00'
                                            b'\x01')
        self.assertIsInstance(st, ServiceTransaction)

    def test_paymenttransaction_serialize(self):
        self.assertIsInstance(self.pt.serialize(), bytes)

    def test_paymenttransaction_deserialize(self):
        pt = PaymentTransaction.deserialize(b'zz!\x002\x00\x00\x00\x01\x00\x00\x00\x12\x06\x05\x00\xe0\xe8\x00\x00\x01\
        xe1\x00\x00\x00\x00\x00\x00\x00@\x1f\x00\x00\x00\x00\x00\x00')
        self.assertIsInstance(pt, PaymentTransaction)

    def test_encashmenttransaction_serialize(self):
        self.assertIsInstance(self.et.serialize(), bytes)

    def test_encashmenttransaction_deserialize(self):
        et = EncashmentTransaction.deserialize(b'zz!\x002\x00\x00\x00\x04\x00\x00\x00\x12\x06\x05\x00\xaa\xe9\x00\x00\x027\
        x02\x00\x00\x00\x00\x00\x00 N\x00\x00\x00\x00\x00\x00')
        self.assertIsInstance(et, EncashmentTransaction)


@pytest.mark.parametrize('transaction, expected', [(ServiceTransaction(100, 100, 'reload'), 0),
                                                   (PaymentTransaction(500, 500, 500, 500, 500), 1),
                                                   (EncashmentTransaction(500, 500, 500, 500), 2)])
def test_transaction_types(transaction, expected):
    assert Transaction.get_type(transaction.serialize()) == expected, 'Incorrect type'


@pytest.mark.parametrize('total_seconds, expected', [(86399, (23, 59, 59)),
                                                     (7825, (2, 10, 25)),
                                                     (43200, (12, 0, 0 ))])
def test_transaction_get_time(total_seconds, expected):
    assert Transaction.get_time(total_seconds) == expected, 'Incorrect get_time function behaviour'


@pytest.mark.parametrize('dict_data, value, expected', [({6: 'asd', 100: '32'}, 'asd', 6),
                                                        ({100: 25, 400: 46}, 25, 100),
                                                        ({'asd': 'fgh', 5: 'asd'}, 'fgh', 'asd')])
def test_servicetransaction_get_key(dict_data, value,  expected):
    assert ServiceTransaction.get_key(dict_data, value) == expected, 'Wrong key of dictionary'
