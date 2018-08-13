import os
import sys
import sqlite3

sys.path.append('..')

from db import DatabaseOrganization, DB

db_tr = DB()
db_trans = db_tr.cursor
db_or = DatabaseOrganization()
db_org = db_or.cursor


def not_implemented():
    print('Not implemented yet!')


def get_org_and_types():
    db_tr = DB()
    db_trans = db_tr.cursor
    db_or = DatabaseOrganization()
    db_org = db_or.cursor
    query = '''SELECT organization.id, 
    organization.name, org_type.name FROM organization INNER JOIN org_type ON organization.type=org_type.id'''
    return db_org.execute(query).fetchall()


def get_terminals():
    query = 'SELECT * FROM terminal'
    return db_trans.execute(query).fetchall()


def get_count(tablename):
    db = get_db(tablename)
    query = 'SELECT COUNT(*) FROM {}'.format(tablename)
    return int(db.execute(query).fetchone()[0])


def get_data(tablename, start=0, count=50):
    db = get_db(tablename)
    query = 'SELECT * FROM {} LIMIT ?, ?'.format(tablename)
    return db.execute(query, (start, count, )).fetchall()


def get_headers(tablename):
    db = get_db(tablename)
    query = 'PRAGMA TABLE_INFO({})'.format(tablename)
    return db.execute(query).fetchall()


def get_organizations():
    query = 'SELECT * FROM organization'
    return db_org.execute(query).fetchall()


def get_org_by_type(type_id):
    db_tr = DB()
    db_trans = db_tr.cursor
    db_or = DatabaseOrganization()
    db_org = db_or.cursor
    query = 'SELECT organization.id, organization.name, org_type.name, organization.logo FROM organization INNER JOIN' \
            ' org_type ON org_type.id=organization.type WHERE organization.type=?'
    return db_org.execute(query, (type_id, )).fetchall()


def get_org_types():
    db_tr = DB()
    db_trans = db_tr.cursor
    db_or = DatabaseOrganization()
    db_org = db_or.cursor
    query = 'SELECT * FROM org_type'
    return db_org.execute(query).fetchall()


def get_transactions():
    query = 'SELECT * FROM ps_transaction'
    return db_trans.execute(query).fetchall()


def get_collectors():
    query = 'SELECT * FROM collector'
    return db_org.execute(query).fetchall()


def update_terminals(table):
    table.table_update(get_terminals(), titles=['ID', 'Last transaction id', 'Cash', 'State'], header='Terminals',
                       tablename='terminal')


def update_organizations(table):
    table.table_update(get_organizations(), titles=['ID', 'Name', 'Commision', 'Type', 'Logo'], header='Organizations',
                       tablename='organization')


def update_types(table):
    table.table_update(get_org_types(), titles=['ID', 'Name'], header='Organization types', tablename='org_type')


def update_trans(table):
    table.table_update(get_transactions(), titles=['Length', 'Term_id', 'Trans_id', 'Date', 'Type', 'Action',
                                                   'Org_id', 'Account', 'Collector id', 'Amount'],
                       header='Transactions', tablename='ps_transaction')


def update_collectors(table):
    table.table_update(get_collectors(), titles=['ID', 'Name', 'Surname', 'Phone', 'Hash'], header='Collectors', tablename=
                       'collector')

def get_db(tname):
    if tname in ['organization', 'collector', 'org_type']:
        return db_or.conn
    elif tname in ['terminal', 'ps_transaction']:
        return db_tr.conn

def get_db_name(tname):
    if tname in ['organization', 'collector', 'org_type']:
        return os.path.basename(DatabaseOrganization.DB_NAME)
    elif tname is 'terminal':
        return os.path.basename(DB.DB_NAME)


def insert(tname, values):
    value_str = '?,' * len(values)
    value_str = value_str[:-1]
    query = 'INSERT INTO {} VALUES ({})'.format(tname, value_str)
    db = get_db(tname)
    db.execute(query, values)
    db.commit()


def delete(tname, values):
    query = 'DELETE FROM {} WHERE id = ?'.format(tname)
    db = get_db(tname)
    db.execute(query, (values[0], ))
    db.commit()


def update(tname, values, _id):
    db = get_db(tname)
    if tname is 'terminal':
        query = 'UPDATE {} SET id=?, last_transaction_id = ?, cash = ?, state = ? WHERE id=?'.format(tname)
    elif tname is 'organization':
        query = 'UPDATE {} SET id=?, name=?, commission=?, type=?, logo=? WHERE id=?'.format(tname)
    elif tname is 'org_type':
        query = 'UPDATE {} SET id=?, name=? WHERE rowid=?'.format(tname)
    elif tname is 'collector':
        query = 'UPDATE {} SET id=?, name=?, surname=?, phone=?, secret=? WHERE id=?'.format(tname)
    try:
        db.execute(query, values +[_id])
        db.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False
    return False

if __name__ == '__main__':
    print(get_org_and_types())
    print(get_org_types())
    print(get_org_by_type(1))
    print(get_headers('terminal'))
    print(get_data('terminal'))
    print(get_count('ps_transaction'))