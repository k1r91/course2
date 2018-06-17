import sys
import unittest
import pytest
sys.path.append('..')
from terminal import TerminalException, Terminal
from transaction import EncashmentTransactionException, ServiceTransactionException, PaymentTransactionException


class TestTerminal(unittest.TestCase):

    def test_terminal_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            with Terminal(1051):
                pass

    def test_not_response(self):
        with self.assertRaises(ConnectionRefusedError):
            with Terminal(1049):
                pass