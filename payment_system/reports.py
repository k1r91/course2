from datetime import datetime

from db import DatabaseOrganization, DB

db_org = DatabaseOrganization()
db_trans = DB()
org_cursor = db_org.conn.cursor()
trans_cursor = db_trans.conn.cursor()


def check_instance(date):
    if date and not isinstance(date, datetime):
        raise TypeError('Parameter {} must be a datetime.datetime class.'.format(date))


def select_transactions_by_var(variable, id, start=None, end=None):
    check_instance(start)
    check_instance(end)
    if start and end and start > end:
        raise ValueError('Start date must be lower than and date')
    if not start and not end:
        query = 'SELECT * FROM ps_transaction WHERE {} = ?'.format(variable)
        result = trans_cursor.execute(query, (id, ))
    elif start and not end:
        query = 'SELECT * FROM ps_transaction WHERE {} = ? AND datetime >= ?'.format(variable)
        result = trans_cursor.execute(query, (id, start))
    elif not start and end:
        query = 'SELECT * FROM ps_transaction WHERE {} = ? AND datetime <= ?'.format(variable)
        result = trans_cursor.execute(query, (id, end))
    else:
        query = 'SELECT * FROM ps_transaction WHERE {} = ? AND datetime >=? AND datetime <= ?'.format(variable)
        result = trans_cursor.execute(query, (id, start,  end))
    return result.fetchall()


def calculate_sum(org_id, start=None, end=None):
    check_instance(start)
    check_instance(end)
    result_trans = select_transactions_by_var('org_id', org_id, start=start, end=end)
    query_org = '''SELECT organization.name, org_type.name FROM organization INNER JOIN org_type on
                organization.type=org_type.id  WHERE organization.id = ?'''
    # the same query as query_org, but instead of join use where statement
    query_org_1 = 'SELECT organization.name, org_type.name FROM organization, org_type WHERE ' \
                  'organization.type=org_type.id AND organization.id = ?'
    result_org = list(org_cursor.execute(query_org, (org_id, )).fetchone())
    org_name, org_type = result_org[0], result_org[1]
    total_amount = sum([item[-1] for item in result_trans]) / 100
    if start and not end:
        end = result_trans[-1][3]
    elif not start and end:
        start = result_trans[0][3]
    elif not start and not end:
        start = result_trans[0][3]
        end = result_trans[-1][3]
    result_str = 'Обороты с организацией {}({}) за период с {} по {} составляют {} рублей'.format(org_name, org_type,
                                                                                                  start, end,
                                                                                                  total_amount)
    return result_str

if __name__ == '__main__':
    select_1 = select_transactions_by_var('term_id', 1049)
    select_2 = select_transactions_by_var('term_id', 1049, start=datetime(year=2018, month=6, day=14))
    select_3 = select_transactions_by_var('term_id', 1049, start=datetime(year=2018, month=6, day=13))
    print(select_1)
    print(select_2)
    print(select_3)
    try:
        select_4 = select_transactions_by_var('term_id', 1049, 'bbbbbbb')
        print(select_4)
    except TypeError as err:
        print(err)
    print(select_1 == select_3)
    select_5 = calculate_sum(10)
    print(select_5)
    select_6 = calculate_sum(15, start=datetime(year=2018, month=6, day=14))
    print(select_6)
    select_7 = calculate_sum(11, start=datetime(year=2018, month=6, day=13), end=datetime(year=2018, month=6, day=13,
                                                                                          hour=14))
    print(select_7)
