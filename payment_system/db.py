import os
import sqlite3


class DB:
    DB_NAME = os.path.join(os.path.dirname(__file__), 'database', 'transactions.db3')

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
    DB_NAME = os.path.join(os.path.dirname(__file__), 'database', 'col_org.db3')

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()

    def set_up(self):
        self.create_table_org_types()
        self.create_table_organizations()
        self.create_table_collectors()
        self.fill_types()
        self.fill_organizations()
        self.fill_collectors()
    
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
                commission TINYINT NOT NULL,
                type TINYINT NOT NULL,
                logo VARCHAR(255) NOT NULL,
                FOREIGN KEY (type) REFERENCES org_type(id)
                )"""
        self.cursor.execute((query))

    def create_table_collectors(self):
        query = """CREATE TABLE IF NOT EXISTS collector(
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                phone VARCHAR(11) NOT NULL,
                secret VARCHAR(64) NOT NULL
                )
                """
        self.cursor.execute(query)

    def fill_types(self):
        query = 'INSERT INTO org_type (id, name) VALUES (?, ?)'
        types = [(1, 'Телефония'), (2, 'Интернет'), (3, 'Телевидение')]
        self.conn.executemany(query, types)
        self.conn.commit()
    
    def fill_organizations(self):
        query = 'INSERT INTO organization (name, commission, type, logo) VALUES (?, ?, ?, ?)'

        def logo(folder_name):
            return os.path.join('organizations_logo', folder_name, 'logo.png')
        organizations = [('МТС', 5, 1, logo('МТС')), ('МТС', 5, 2, logo('МТС')), ('МТС', 5, 3, logo('МТС')),
                         ('Билайн', 0, 1, logo('Билайн')), ('Билайн', 0, 2, logo('Билайн')), ('Билайн', 0, 3, logo('Билайн')),
                         ('Мегафон', 10, 1, logo('Мегафон')), ('Мегафон', 10, 2, logo('Мегафон')), ('Акадо-Урал', 1, 3, logo('Акадо-Урал')),
                         ('Мотив', 1, 1, logo('Мотив')), ('Ростелеком', 1, 2, logo('Ростелеком')), ('Планета', 1, 3, logo('Планета')),
                         ('Теле2', 1, 1, logo('Теле2')), ('Кабинет', 1, 2, logo('Кабинет')), ('Convex', 1, 3, logo('Convex')),
                         ('Utel', 1, 1, logo('Utel')), ('Акадо-Урал', 1, 2, logo('Акадо-Урал')), ('ДомРу', 1, 3, logo('ДомРу')),
                         ('Yota', 1, 1, logo('Yota')), ('Планета', 1, 2, logo('Планета')), ('Инсис', 1, 3, logo('Инсис')),
                         ('Таттелеком', 1, 1, logo('Таттелеком')), ('Convex', 1, 2, logo('Convex')), ('РусКом', 1, 3, logo('РусКом')),
                         ('Вайнах Телеком', 1, 1, logo('Вайнах Телеком')), ('ДомРу', 1, 2, logo('ДомРу')), ('Ростелеком', 1, 3, logo('Ростелеком')),
                         ('VK Mobile', 1, 1, logo('VK Mobile')), ('Инсис', 1, 2, logo('Инсис')), ('ТелеКарта', 1, 3, logo('ТелеКарта')),
                         ]
        self.cursor.executemany(query, organizations)
        self.conn.commit()

    def fill_collectors(self):
        query = '''INSERT INTO collector (id, name, surname, phone, secret) VALUES (?, ?, ?, ?, ?)'''
        collectors = [(488, 'Kirill', 'Cherkasov', '89049864438',
                       '9d6fa611b10c4a7ac6b68f953bbc536c4c45b8a4bc0fd215a5bf44254bc454d8'),
                      (1227, 'Larisa', 'Cherkasova', '89097019023',
                       '9d6fa611b10c4a7ac6b68f953bbc536c4c45b8a4bc0fd215a5bf44254bc454d8'),
                      ]
        self.cursor.executemany(query, collectors)
        self.conn.commit()

        
    @staticmethod
    def flush():
        if os.path.exists(DatabaseOrganization.DB_NAME):
            os.remove(DatabaseOrganization.DB_NAME)

if __name__ == '__main__':
    # DB.flush()
    DatabaseOrganization.flush()
    # db = DB()
    # db.set_up()
    dborg = DatabaseOrganization()
    dborg.set_up()
