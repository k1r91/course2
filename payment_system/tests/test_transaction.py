import sys
import unittest
import pytest
sys.path.append('..')
from transaction import Transaction, SerializeException


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.t = Transaction()

