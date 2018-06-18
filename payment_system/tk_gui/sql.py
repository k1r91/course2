import sys

sys.path.append('..')

from db import DatabaseOrganization, DB


db_trans = DB().cursor
db_org = DatabaseOrganization().cursor

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

def perform_query(tablename, values):
    print('Update {} on {}'.format(tablename, values))