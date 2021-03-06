import os
from datetime import datetime
from collections import OrderedDict
from deco import time_it

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
    if not start:
        query = '''SELECT datetime FROM ps_transaction LIMIT 1'''
        datetime_data = trans_cursor.execute(query).fetchone()[0]
        start = datetime.strptime(datetime_data, '%Y-%m-%d  %H:%M:%S')
    if not end:
        end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = 'SELECT * FROM ps_transaction WHERE {} = ? AND datetime >=? AND datetime <= ? AND type = 1'.format(variable)
    result = trans_cursor.execute(query, (id, start,  end))
    data = result.fetchall()
    return data, start, end


def select_all_transactions(start=None, end=None):
    if start and end and start > end:
        raise ValueError('Start date must be lower than and date')
    if not start:
        query = '''SELECT datetime FROM ps_transaction LIMIT 1'''
        datetime_data = trans_cursor.execute(query).fetchone()[0]
        start = datetime.strptime(datetime_data, '%Y-%m-%d  %H:%M:%S')
    if not end:
        end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = 'SELECT * FROM ps_transaction WHERE datetime >=? AND datetime <= ? AND type = 1'
    result = trans_cursor.execute(query, (start, end))
    data = result.fetchall()
    result = list()
    result.append(['Term_id', 'Transaction_id', 'Datetime', 'Org_id', 'Amount', 'Account'])
    for record in data:
        result.append([record[1], record[2], record[3], record[6], record[7], record[9]])
    return result


def select_transactions_by_term(_id, start=None, end=None):
    data, start, end = select_transactions_by_var('term_id', _id, start=start, end=end)
    if not data:
        return [[_id, start, end], None]
    result = [[_id, start, end]]
    result.append(['Transaction_id', 'Datetime', 'Org_id', 'Amount', 'Account'])
    for record in data:
        result.append([
            record[2],
            record[3],
            record[6],
            record[7],
            record[9],
        ])
    return result


def calculate_sum(org_id, start=None, end=None):
    """
    calcucalate debt for one organization
    :param org_id:
    :param start: start of date period
    :param end:  end of date period
    :return: report string
    """
    check_instance(start)
    check_instance(end)
    result_trans, start, end = select_transactions_by_var('org_id', org_id, start=start, end=end)
    query_org = '''SELECT organization.name, org_type.name FROM organization INNER JOIN org_type on
                organization.type=org_type.id  WHERE organization.id = ?'''
    # the same query as query_org, but instead of join use where statement
    query_org_1 = 'SELECT organization.name, org_type.name FROM organization, org_type WHERE ' \
                  'organization.type=org_type.id AND organization.id = ?'
    result_org = list(org_cursor.execute(query_org, (org_id, )).fetchone())
    org_name, org_type = result_org[0], result_org[1]
    total_amount = sum([item[-1] for item in result_trans]) / 100
    result_str = 'Turnover with organization {} ({}) from {} to {}:  {} rubles'.format(org_name, org_type,
                                                                                                  start, end,
                                                                                                  total_amount)
    return result_str


@time_it
def total_calculate_sum(start=None, end=None):
    """
    calculates debt for all organizations
    :param start: date period start
    :param end: date period end
    :return: report string
    """
    check_instance(start)
    check_instance(end)
    result = OrderedDict()
    query = '''SELECT organization.id, organization.name, org_type.name FROM organization INNER JOIN org_type ON
            organization.type = org_type.id'''
    organizations = org_cursor.execute(query).fetchall()
    if not start:
        query = '''SELECT datetime FROM ps_transaction LIMIT 1'''
        datetime_data = trans_cursor.execute(query).fetchone()[0]
        start = datetime.strptime(datetime_data, '%Y-%m-%d  %H:%M:%S')
    if not end:
        end = datetime.now()
    if start > end:
        raise ValueError('Start date must be lower than end date.')
    query = '''SELECT * FROM ps_transaction WHERE datetime >= ? AND datetime <= ? AND type = 1 ORDER BY org_id'''
    transactions = trans_cursor.execute(query, (start, end, )).fetchall()
    for item in organizations:
        sum_org = 0
        for tr in transactions:
            if item[0] == tr[6]:
                sum_org += tr[-1]
        result[item] = sum_org / 100
    report_data = [[start, end]]
    report_data.append(['ID', 'Name', 'Type', 'Amount'])
    for key, value in result.items():
        report_data.append([key[0], key[1], key[2], value])
    return report_data


# @time_it
def total_calculate_sum_v2(org_id=None, start=None, end=None):
    """
    calculates debt for all organizations
    :param start: date period start
    :param end: date period end
    :return: report string
    """
    check_instance(start)
    check_instance(end)
    result = OrderedDict()
    query = '''SELECT organization.id, organization.name, org_type.name FROM organization INNER JOIN org_type ON
            organization.type = org_type.id'''
    if org_id is not None:
        query += ' WHERE organization.id={}'.format(org_id)
    organizations = org_cursor.execute(query).fetchall()
    if not start:
        query = '''SELECT datetime FROM ps_transaction LIMIT 1'''
        datetime_data = trans_cursor.execute(query).fetchone()[0]
        start = datetime.strptime(datetime_data, '%Y-%m-%d  %H:%M:%S')
    if not end:
        end = datetime.now()
    if start > end:
        raise ValueError('Start date must be lower than end date.')
    query = '''SELECT * FROM ps_transaction WHERE datetime >= ? AND datetime <= ? AND type = 1 ORDER BY org_id'''
    transactions = trans_cursor.execute(query, (start, end, )).fetchall()
    for item in organizations:
        trs = [tr for tr in transactions if item[0] == tr[6]]
        sum_org = sum([tr[-1] for tr in trs])
        result[item] = sum_org / 100
    total = [['Organization name', 'Organization type', 'Indebtedness']]
    for key, value in result.items():
        # print('{}. {} ({}): {} рублей.'.format(key[0], key[1], key[2], value))
        total.append([key[1], key[2], value])
    return total


def calculate_sum_by_term(id, start=None, end=None):
    trs, start, end = select_transactions_by_var('term_id', id, start, end)
    sum_term = sum([tr[-1] for tr in trs]) / 100
    if trs:
        return 'Turnover on terminal №{} from {} to {}: {} rubles.'.format(id, start, end, sum_term)
    return 'There are no transaction data.'

def calculate_sum_by_term_v2(id, start=None, end=None):
    trs, start, end = select_transactions_by_var('term_id', id, start, end)
    sum_term = sum([tr[-1] for tr in trs]) / 100
    return [id, sum_term]


def calculate_sum_by_all_terms(start=None, end=None):
    query = 'SELECT id FROM terminal'
    terminals = [x[0] for x in db_trans.cursor.execute(query).fetchall()]
    result = [['Terminal', 'Amount']]
    for t in terminals:
        result.append(calculate_sum_by_term_v2(t, start, end))
    return result

def timespan_report(term_id, spans, start=None, end=None):
    trs, start, end = select_transactions_by_var('term_id', term_id, start, end)
    if not trs:
        return 'Terminal {} has no data'.format(term_id)
    report = OrderedDict()
    for span in spans[:]:
        if spans.index(span) != len(spans) - 1:
            hstart = span
            hend = spans[spans.index(span) + 1]
            count = 0
            for tr in trs:
                date = datetime.strptime(tr[3], '%Y-%m-%d %H:%M:%S')
                if hstart <= date.hour <= hend:
                    count += 1
            report['{}-{}'.format(hstart, hend)] = count
    result = ['Timespan report for terminal {} from {} to {}:'.format(term_id, start, end)]
    for key, value in report.items():
        result.append('{}: {} transactions.'.format(key, value))
    return os.linesep.join(result)


def timespan_report_v2(term_id, spans, start=None, end=None):
    trs, start, end = select_transactions_by_var('term_id', term_id, start, end)
    if not trs:
        return []
    report = OrderedDict()
    for span in spans[:]:
        if spans.index(span) != len(spans) - 1:
            hstart = span
            hend = spans[spans.index(span) + 1]
            count = 0
            for tr in trs:
                date = datetime.strptime(tr[3], '%Y-%m-%d %H:%M:%S')
                if hstart <= date.hour <= hend:
                    count += 1
            report['{}-{}'.format(hstart, hend)] = count

    result = [['Terminal', 'Span (day hour range)', 'Transactions']]
    for key, value in report.items():
        result.append([term_id, key, value])
    return result

if __name__ == '__main__':
    # select_1 = select_transactions_by_term(1049)
    # select_2 = select_transactions_by_term(1049, start=datetime(year=2018, month=6, day=14))
    # select_3 = select_transactions_by_term(1049, start=datetime(year=2018, month=6, day=13))
    # print(select_1)
    # print(select_2)
    # print(select_3)
    # try:
    #     select_4 = select_transactions_by_term(1049, 'bbbbbbb')
    #     print(select_4)
    # except TypeError as err:
    #     print(err)
    # print(select_1 == select_3)
    # select_5 = calculate_sum(10, start=datetime(year=2018, month=6, day=14))
    # print(select_5)
    # select_6 = calculate_sum(15, start=datetime(year=2018, month=6, day=14))
    # print(select_6)
    # select_7 = calculate_sum(11, start=datetime(year=2018, month=6, day=13), end=datetime(year=2018, month=6, day=13,
    #                                                                                       hour=14))
    # print(select_7)
    # print(total_calculate_sum(start=datetime(year=2018, month=6, day=14)))
    print(calculate_sum_by_term_v2(1049))
    print(calculate_sum_by_all_terms())
    # print(timespan_report_v2(250, (0, 6, 12, 18, 24)))
    # print(timespan_report(45, (0, 6, 12, 18, 24)))
    # print(timespan_report(304, (0, 3, 6, 9, 12, 15, 18, 24)))
    # print(total_calculate_sum_v2())
