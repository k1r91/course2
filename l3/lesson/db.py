import sqlite3

conn = sqlite3.connect('company.db3')
cursor = conn.cursor()
query = """CREATE TABLE IF NOT EXISTS terminal (
        id INTEGER PRIMARY KEY,
        configuration TEXT,
        title VARCHAR(128)
        )"""
cursor.execute(query)


try:
    cursor.execute(query, (13, 'configuration_13', 'title_13'))
except sqlite3.IntegrityError:
    pass
cursor.execute('SELECT * FROM terminal')
z = cursor.fetchone()
while z:
    print(z)
    z = cursor.fetchone()
