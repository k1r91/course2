import sys
import unittest
import sqlite3
sys.path.append('..')

from db import DB, DatabaseOrganization


class TestDb(unittest.TestCase):
    def setUp(self):
        self.db_trans = DB()
        self.db_org = DatabaseOrganization()

    def test_db_trans_already_filled(self):
        """To pass test, run first db.py
        """
        with self.assertRaises(sqlite3.IntegrityError):
            self.db_trans.fill_terminal()

    def test_db_org_already_filled(self):
        """To pass test, run first db.py
        """
        with self.assertRaises(sqlite3.IntegrityError):
            self.db_org.fill_collectors()