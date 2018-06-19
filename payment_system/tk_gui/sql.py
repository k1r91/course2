import sys

sys.path.append('..')

from db import DatabaseOrganization, DB

db_tr = DB()
db_trans = db_tr.cursor
db_or = DatabaseOrganization()
db_org = db_or.cursor

def not_implemented():
    print('Not implemented yet!')


def get_terminals():
    query = 'SELECT * FROM terminal'
    return db_trans.execute(query).fetchall()


def get_organizations():
    query = 'SELECT * FROM organization'
    return db_org.execute(query).fetchall()


def get_org_types():
    query = 'SELECT * FROM org_type'
    return db_org.execute(query).fetchall()


def get_transactions():
    query = 'SELECT * FROM ps_transaction LIMIT 10'
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
    elif tname is 'terminal':
        return db_tr.conn

def get_db_name(tname):
    if tname in ['organization', 'collector', 'org_type']:
        return DatabaseOrganization.DB_NAME
    elif tname is 'terminal':
        return DB.DB_NAME


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

def update(tname, values, row_id):
    db = get_db(tname)
    if tname is 'terminal':
        query = 'UPDATE {} SET id = ?, last_transaction_id = ?, cash = ?, state = ? WHERE rowid = ?'.format(tname)
    elif tname is 'organization':
        query = 'UPDATE {} SET id=?, name=?, commission=?, type=?, logo=? WHERE rowid=?'.format(tname)
    elif tname is 'org_type':
        query = 'UPDATE {} SET id=?, name=? WHERE rowid=?'.format(tname)
    elif tname is 'collector':
        query = 'UPDATE {} SET id=?, name=?, surname=?, phone=?, secret=? WHERE rowid=?'.format(tname)
    db.execute(query, values + [row_id+1])
    db.commit()