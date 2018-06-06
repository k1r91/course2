import os
import sqlite3

from transaction import Transaction
from terminal import Terminal


class DB:
    DB_NAME = os.path.join('database', 'global.db3')

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()

    def set_up(self):
        self.create_table_collectors()
        self.create_table_organizations()
        self.create_table_terminal()
        self.create_table_transaction()
        self.fill_terminal()

    def create_table_collectors(self):

        query = """CREATE TABLE collector(
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                phone VARCHAR(11) NOT NULL
                )
                """
        self.cursor.execute((query))

    def create_table_organizations(self):
        query = """CREATE TABLE organization (
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                bill BIGINT NOT NULL DEFAULT 0
                )"""
        self.cursor.execute((query))

    def create_table_terminal(self):
        query = """CREATE TABLE terminal (
                id INT PRIMARY KEY,
                last_transaction_id INT NOT NULL DEFAULT 0,
                cash BIGINT NOT NULL DEFAULT 0,
                state TINYINT NOT NULL DEFAULT 1
                )"""
        self.cursor.execute(query)

    def create_table_transaction(self):
        query = """CREATE TABLE IF NOT EXISTS {} (
                length SMALLINT NOT NULL,
                term_id INTEGER NOT NULL,
                transaction_id BIGINT NOT NULL,
                datetime DATE NOT NULL,
                type TINYINT NOT NULL,
                action VARCHAR(255),
                org_id INT,
                collector_id INT,
                amount BIGINT,
                FOREIGN KEY (term_id) REFERENCES terminal(id),
                FOREIGN KEY (org_id) REFERENCES organization(id),
                FOREIGN KEY (collector_id) REFERENCES collector(id)
                )""".format(Transaction.__tablename__)
        self.cursor.execute(query)

    def fill_terminal(self):
        terminals = [(7, ), (55, ), (250, ), (304, ), (1049, )]
        query = 'INSERT INTO terminal (id) VALUES (?)'
        self.cursor.executemany(query, terminals)
        self.conn.commit()
    @staticmethod
    def flush():
        if os.path.exists(DB.DB_NAME):
            os.remove(DB.DB_NAME)


if __name__ == '__main__':
    DB.flush()
    db = DB()
    db.set_up()
