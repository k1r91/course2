import os
import sqlite3


class DB:
    DB_NAME = os.path.join('database', 'transactions.db3')

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()

    def set_up(self):
        self.create_table_terminal()
        self.create_table_transaction()
        self.fill_terminal()

    def create_table_terminal(self):
        query = """CREATE TABLE IF NOT EXISTS terminal (
                id INT PRIMARY KEY,
                last_transaction_id INT NOT NULL DEFAULT 0,
                cash BIGINT NOT NULL DEFAULT 0,
                state TINYINT NOT NULL DEFAULT 1
                )"""
        self.cursor.execute(query)

    def create_table_transaction(self):
        query = """CREATE TABLE IF NOT EXISTS ps_transaction (
                length SMALLINT NOT NULL,
                term_id INTEGER NOT NULL,
                transaction_id BIGINT NOT NULL,
                datetime DATE NOT NULL,
                type TINYINT NOT NULL,
                action VARCHAR(255),
                org_id INT,
                account BIGINT,
                collector_id INT,
                amount BIGINT,
                FOREIGN KEY (term_id) REFERENCES terminal(id)
                )"""
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


class DatabaseOrganization:
    DB_NAME = os.path.join('database', 'col_org.db3')

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()

    def set_up(self):
        self.create_table_org_types()
        self.create_table_organizations()
        self.create_table_collectors()
        self.fill_types()
        self.fill_organizations()
    
    def create_table_org_types(self):
        query = """CREATE TABLE IF NOT EXISTS org_type(
                id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL
                )"""
        self.cursor.execute(query)
    
    def create_table_organizations(self):
        query = """CREATE TABLE IF NOT EXISTS organization (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                type INTEGER NOT NULL,
                logo VARCHAR(255) NOT NULL,
                FOREIGN KEY (type) REFERENCES org_type(id)
                )"""
        self.cursor.execute((query))

    def create_table_collectors(self):
        query = """CREATE TABLE IF NOT EXISTS collector(
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                phone VARCHAR(11) NOT NULL
                )
                """
        self.cursor.execute(query)

    def fill_types(self):
        query = 'INSERT INTO org_type (id, name) VALUES (?, ?)'
        types = [(1, 'Телефония'), (2, 'Интернет'), (3, 'Телевидение')]
        self.conn.executemany(query, types)
        self.conn.commit()
    
    def fill_organizations(self):
        query = 'INSERT INTO organization (name, type, logo) VALUES (?, ?, ?)'

        def logo(folder_name):
            return os.path.join('organizations_logo', folder_name, 'logo.png')
        organizations = [('МТС', 1, logo('МТС')), ('МТС', 2, logo('МТС')), ('МТС', 3, logo('МТС')),
                         ('Билайн', 1, logo('Билайн')), ('Билайн', 2, logo('Билайн')), ('Билайн', 3, logo('Билайн')),
                         ('Мегафон', 1, logo('Мегафон')), ('Мегафон', 2, logo('Мегафон')), ('Акадо-Урал', 3, logo('Акадо-Урал')),
                         ('Мотив', 1, logo('Мотив')), ('Ростелеком', 2, logo('Ростелеком')), ('Планета', 3, logo('Планета')),
                         ('Теле2', 1, logo('Теле2')), ('Кабинет', 2, logo('Кабинет')), ('Convex', 3, logo('Convex')),
                         ('Utel', 1, logo('Utel')), ('Акадо-Урал', 2, logo('Акадо-Урал')), ('ДомРу', 3, logo('ДомРу')),
                         ('Yota', 1, logo('Yota')), ('Планета', 2, logo('Планета')), ('Инсис', 3, logo('Инсис')),
                         ('Таттелеком', 1, logo('Таттелеком')), ('Convex', 2, logo('Convex')), ('РусКом', 3, logo('РусКом')),
                         ('Вайнах Телеком', 1, logo('Вайнах Телеком')), ('ДомРу', 2, logo('ДомРу')), ('Ростелеком', 3, logo('Ростелеком')),
                         ('VK Mobile', 1, logo('VK Mobile')), ('Инсис', 2, logo('Инсис')), ('ТелеКарта', 3, logo('ТелеКарта')),
                         ]
        self.cursor.executemany(query, organizations)
        self.conn.commit()

        
    @staticmethod
    def flush():
        if os.path.exists(DatabaseOrganization.DB_NAME):
            os.remove(DatabaseOrganization.DB_NAME)

if __name__ == '__main__':
    DB.flush()
    db = DB()
    db.set_up()
    DatabaseOrganization.flush()
    dborg = DatabaseOrganization()
    dborg.set_up()
