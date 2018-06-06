import datetime
import sys
import struct


class SerializeException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


class ServiceTransactionException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


class Transaction:

    __tablename__ = 'ps_transaction'

    header = 0x7a7a
    PACK_FORMAT = 'HBIIHIB'
    TYPE = 0x00

    def __init__(self, term_id, tr_id):
        self.term_id = term_id
        self.tr_id = tr_id
        # self.date = None        # attribute defined in deserialize method
        # self.length = None      # attribute defined in deserialize method
        # self.type = 0x00

    def get_length(self):
        """
        >>> t = Transaction(100, 100)
        >>> t.get_length()
        17

        :return: length of transaction data
        """
        year, month, day, seconds = Transaction.get_datetime()
        packed_date = self.pack_data(year, month, day)
        self.length = len(struct.pack(Transaction.PACK_FORMAT[2:], self.term_id, self.tr_id, packed_date, seconds,
                                      self.TYPE))
        return self.length

    def serialize(self, length, tr_type):
        """
        Serializes transaction for network transmission
        :param length: length of transaction data
        :param tr_type: transaction type
        :return: binary string created by struct.pack module according to hex PACK_FORMAT
        """
        year, month, day, seconds = Transaction.get_datetime()
        packed_date = self.pack_data(year, month, day)
        result = struct.pack(Transaction.PACK_FORMAT, self.header, length, self.term_id, self.tr_id, packed_date,
                             seconds, tr_type)
        return result


    @staticmethod
    def deserialize(data):
        """
        :param data: binary string created by struct.pack module according to PACK_FORMAT value
        :return: unpacked data in dictionary
        """
        result = {}
        data = struct.unpack(Transaction.PACK_FORMAT, data[:Transaction.fmt_size()])
        Transaction.check_header(data[0])
        result['header'] = data[0]
        result['length'] = data[1]
        result['term_id'] = data[2]
        result['tr_id'] = data[3]
        year, month, day = Transaction.unpack_data(data[4])
        hour, minute, second = Transaction.get_time(data[5])
        result['date'] = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        result['type'] = data[6]
        return result

    @staticmethod
    def get_type(data):
        """
        >>> Transaction.get_type(ServiceTransaction(500, 500, 'reload').serialize())
        0
        >>> Transaction.get_type(PaymentTransaction(500, 500, 500, 500).serialize())
        1

        :param data: binary string in hex format according to PACK_FORMAT
        :return: transaction type: 0 - service, 1 - payment, 2 - encashment
        """
        data = struct.unpack(Transaction.PACK_FORMAT, data[:Transaction.fmt_size()])
        return data[-1]

    @staticmethod
    def get_datetime():
        """
        :return: year, month, day, seconds(since midnight) tuple
        """
        now = datetime.datetime.now()
        year = now.year
        seconds = Transaction.seconds_since_midnight()
        return year, now.month, now.day, seconds

    @staticmethod
    def get_time(tseconds):
        """
        >>> Transaction.get_time(86399)
        (23, 59, 59)
        >>> Transaction.get_time(3665)
        (1, 1, 5)

        :param tseconds: total seconds
        :return: hours, minutes and seconds of total seconds seconds
        """
        hours = tseconds // 3600
        minutes = (tseconds - hours*3600) // 60
        seconds = tseconds - hours*3600 - minutes*60
        return hours, minutes, seconds

    @staticmethod
    def seconds_since_midnight():
        """
        :return: seconds since midnight
        """
        now = datetime.datetime.now()
        midnight = datetime.datetime.combine(now.date(), datetime.time())
        seconds = (now - midnight).seconds
        return seconds

    @staticmethod
    def pack_data(year, month, day, year_sz=7, month_sz=4, day_sz=5):
        """
        Packs current date in integer value, by default no more than 2 bytes
        :param year: current year
        :param month: current month
        :param day: current day
        :param year_sz: size in bits to pack year
        :param month_sz: size in bits to pack month
        :param day_sz: size in bits to pack day
        :return: packed integer value of data
        """
        year -= 2000
        if year > 2 ** year_sz:
            raise ValueError("Year is too big to pack in {} bits.".format(year_sz))
        if month > 2 ** month_sz:
            raise ValueError("Month is too big to pack in {} bits.".format(month_sz))
        if day > 2 ** day_sz:
            raise ValueError("Day is too big to pack in {} bits.".format(day_sz))
        year_str = str(bin(year))[2:].zfill(year_sz)
        month_str = str(bin(month))[2:].zfill(month_sz)
        day_str = str(bin(day))[2:].zfill(day_sz)
        return int(''.join([year_str, month_str, day_str]), 2)

    @staticmethod
    def unpack_data(value, year_sz=7, month_sz=4, day_sz=5):
        """
        Unpack packed integer value of date to year, month and day according to sizes
        :param value: packed integer value of date
        :param year_sz: size in bits of packed year
        :param month_sz: size in bits of packed month
        :param day_sz: size in bits of packed day
        :return: (year, month, day) tuple
        """
        raw_str = str(bin(value))[2:].zfill(year_sz+month_sz+day_sz)
        year = int(raw_str[:year_sz], 2)
        year += 2000
        month = int(raw_str[year_sz:year_sz+month_sz], 2)
        day = int(raw_str[year_sz+month_sz:year_sz+month_sz+day_sz], 2)
        return year, month, day

    @staticmethod
    def check_header(header):
        """
        >>> Transaction.check_header(0x7a7a)
        True

        :param header:
        :return: True if header correct
        """
        if header != Transaction.header:
            raise ValueError('Header is incorrect!')
        return True

    @staticmethod
    def fmt_size():
        """
        :return: size of packed data according to PACK_FORMAT
        """
        return struct.calcsize(Transaction.PACK_FORMAT)

    def __str__(self):
        return 'length={}, date={}, tr_id={}, terminal_id={}'.format(self.length, self.date, self.tr_id, self.term_id)


class ServiceTransaction(Transaction):
    data = {'power_on': 0x00,
            'reload': 0x01,
            'shutdown': 0x02,
            'activate_sensor': 0x03,
            'block': 0x04
            }
    TYPE = 0x00
    PACK_FORMAT = 'BIQB'

    def __init__(self, term_id, tr_id, action, term_config=None):
        super().__init__(term_id, tr_id)
        self.action = self.data[action]
        self.term_config = term_config
        try:
            self.last_transaction_id = term_config['last_transaction_id']
            self.cash = term_config['cash']
            self.state = term_config['state']
        except (IndexError, TypeError):
            raise ServiceTransactionException('''Incorrect service transaction: with power_on, reload or shutdown
                                                    action you should transmit proper terminal configuration''')
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.action, self.last_transaction_id,
                                                             self.cash, self.state))

    def serialize(self):
        """
        date is determined dynamically
        :return: binary hex string according to pack format
        """
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.action,
                                                                             self.last_transaction_id, self.cash,
                                                                             self.state)
        return result

    @staticmethod
    def deserialize(data):
        """
        :param data: binary string in hex format
        :return: new ServiceTransaction exemplary with filled parameters
        """
        parent_data = Transaction.deserialize(data[:Transaction.fmt_size()])
        ServiceTransaction.check_type(parent_data['type'])
        data = struct.unpack(ServiceTransaction.PACK_FORMAT, data[-ServiceTransaction.fmt_size():])
        action = ServiceTransaction.get_key(ServiceTransaction.data, data[0])
        tr_id = parent_data['tr_id']
        term_id = parent_data['term_id']
        term_config = {'last_transaction_id': data[1], 'cash': data[2], 'state': data[3]}
        res = ServiceTransaction(term_id, tr_id, action, term_config=term_config)
        res.length = parent_data['length']
        res.date = parent_data['date']
        return res

    @staticmethod
    def get_key(dict_data, value):
        """
        >>> ServiceTransaction.get_key({5: 'asd', 6: 'fgh'}, 'asd')
        5

        :param dict_data: dictionary
        :param value: we try to find key of this value
        :return: key
        """
        for key, _value in dict_data.items():
            if _value == value:
                return key

    @staticmethod
    def check_type(ttype):
        if ttype != ServiceTransaction.TYPE:
            raise ValueError('Type is incorrect')

    @staticmethod
    def fmt_size():
        return struct.calcsize(ServiceTransaction.PACK_FORMAT)

    def __str__(self):
        return 'Service transaction: {}, action={},' \
               'terminal_configuration={}'.format(super().__str__(), self.get_key(self.data, self.action),
                                                  self.term_config)


class PaymentTransaction(Transaction):
    TYPE = 0x01
    PACK_FORMAT = 'IQ'

    def __init__(self, term_id, tr_id, org_id, amount):
        super().__init__(term_id, tr_id)
        self.org_id = org_id
        self.amount = amount
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.org_id, self.amount))

    def serialize(self):
        """
        :return: binary hex string according to pack format
        """
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.org_id, self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """
        :param data: binary hex string according to pack format
        :return: new PaymentTransaction exemplary with filled parameters
        """
        parent_data = Transaction.deserialize(data[:Transaction.fmt_size()])
        PaymentTransaction.check_type(parent_data['type'])
        data = struct.unpack(PaymentTransaction.PACK_FORMAT, data[-PaymentTransaction.fmt_size():])
        tr_id = parent_data['tr_id']
        term_id = parent_data['term_id']
        org_id = data[0]
        amount = data[1]
        res = PaymentTransaction(term_id, tr_id, org_id, amount)
        res.length = parent_data['length']
        res.date = parent_data['date']
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != PaymentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    @staticmethod
    def fmt_size():
        return struct.calcsize(PaymentTransaction.PACK_FORMAT)

    def __str__(self):
        return 'Payment transaction: {}, org_id={}, amount={}'.format(super().__str__(), self.org_id, self.amount)


class EncashmentTransaction(Transaction):

    PACK_FORMAT = 'IQ'
    TYPE = 0x02

    def __init__(self, term_id, tr_id, collector_id, amount):
        super().__init__(term_id, tr_id)
        self.collector_id = collector_id
        self.amount = amount
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.collector_id, self.amount))

    def serialize(self):
        """
        :return: binary hex string according to pack format
        """
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.collector_id,
                                                                         self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """
        :param data: binary hex string according to pack format
        :return: new EncashmenttTransaction exemplary with filled parameters
        """
        parent_data = Transaction.deserialize(data[:Transaction.fmt_size()])
        EncashmentTransaction.check_type(parent_data['type'])
        data = struct.unpack(PaymentTransaction.PACK_FORMAT, data[-EncashmentTransaction.fmt_size():])
        collector_id = data[0]
        amount = data[1]
        term_id = parent_data['term_id']
        tr_id = parent_data['tr_id']
        res = EncashmentTransaction(term_id, tr_id, collector_id, amount)
        res.length = parent_data['length']
        res.date = parent_data['date']
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != EncashmentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    @staticmethod
    def fmt_size():
        return struct.calcsize(EncashmentTransaction.PACK_FORMAT)

    def __str__(self):
        return 'Encashment transaction: {}, collector_id={}, amount={}'.format(super().__str__(), self.collector_id,
                                                                               self.amount)


if __name__ == '__main__':
    def print_transaction(tr):
        tr_serialized = tr.serialize()
        print('Serialized transaction: {}'.format(tr_serialized))
        print('Serialized size: {} bytes'.format(sys.getsizeof(tr_serialized)))
        print('Deserialized info: {}'.format(tr.deserialize(tr_serialized)))
        print('Type: {}'.format(Transaction.get_type(tr_serialized)))
        print('*' * 40)
    print_transaction(PaymentTransaction(50, 1, 225, 8000))
    print_transaction(ServiceTransaction(50, 2, 'power_on', {'last_transaction_id':25,'cash':5000, 'state':1}))
    print_transaction(ServiceTransaction(50, 3, 'activate_sensor', {'last_transaction_id':25,'cash':5000, 'state':1}))
    print_transaction(EncashmentTransaction(50, 4, 567, 20000))
    pass
