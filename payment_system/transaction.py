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


class Transaction:

    header = 0x7a7a
    PACK_FORMAT = 'HBIIBBBIB'
    TYPE = 0x00

    def __init__(self, term_id, tr_id):
        self.term_id = term_id
        self.tr_id = tr_id
        # self.date = None        # attribute defined in deserialize method
        # self.length = None      # attribute defined in deserialize method
        # self.type = 0x00

    def get_length(self):
        year, month, day, seconds = Transaction.get_datetime()
        self.length = len(struct.pack(Transaction.PACK_FORMAT[2:], self.term_id, self.tr_id, year, month, day, seconds,
                                      self.TYPE))
        return self.length

    def serialize(self, length, tr_type):
        year, month, day, seconds = Transaction.get_datetime()
        result = struct.pack(Transaction.PACK_FORMAT, self.header, length, self.term_id, self.tr_id, year, month, day,
                             seconds, tr_type)
        return result

    @staticmethod
    def deserialize(data):
        result = {}
        data = struct.unpack(Transaction.PACK_FORMAT, data[:Transaction.fmt_size()])
        Transaction.check_header(data[0])
        result['header'] = data[0]
        result['length'] = data[1]
        result['term_id'] = data[2]
        result['tr_id'] = data[3]
        year = data[4] + 2000
        month = data[5]
        day = data[6]
        hour, minute, second = Transaction.get_time(data[7])
        result['date'] = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        result['type'] = data[8]
        return result

    @staticmethod
    def get_type(data):
        data = struct.unpack(Transaction.PACK_FORMAT, data[:Transaction.fmt_size()])
        return data[-1]

    @staticmethod
    def get_datetime():
        now = datetime.datetime.now()
        year = now.year - 2000
        seconds = Transaction.seconds_since_midnight()
        return year, now.month, now.day, seconds

    @staticmethod
    def get_time(tseconds):
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
    def check_header(header):
        if header != Transaction.header:
            raise ValueError('Header is incorrect!')

    @staticmethod
    def fmt_size():
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
    PACK_FORMAT = 'B'

    def __init__(self, term_id, tr_id, action):
        super().__init__(term_id, tr_id)
        self.action = self.data[action]

    def serialize(self):
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.action))
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.action)
        return result

    @staticmethod
    def deserialize(data):
        """
        returns new ServiceTransaction exemplary with filled parameters
        :param data:
        :return:
        """
        parent_data = Transaction.deserialize(data[:Transaction.fmt_size()])
        ServiceTransaction.check_type(parent_data['type'])
        data = struct.unpack(ServiceTransaction.PACK_FORMAT, data[-ServiceTransaction.fmt_size():])
        action = ServiceTransaction.get_key(ServiceTransaction.data, data[0])
        tr_id = parent_data['tr_id']
        term_id = parent_data['term_id']
        res = ServiceTransaction(term_id, tr_id, action)
        res.length = parent_data['length']
        res.date = parent_data['date']
        return res

    @staticmethod
    def get_key(dict_data, value):
        for key, _value in dict_data.items():
            if _value == value:
                return key

    @staticmethod
    def check_type(ttype):
        if ttype != ServiceTransaction.TYPE:
            raise ValueError('Type is incorrect')

    def __str__(self):
        return 'Service transaction: {}, action={}'.format(super().__str__(), self.get_key(self.data, self.action))

    @staticmethod
    def fmt_size():
        return struct.calcsize(ServiceTransaction.PACK_FORMAT)


class PaymentTransaction(Transaction):
    TYPE = 0x01
    PACK_FORMAT = 'IQ'

    def __init__(self, term_id, tr_id, org_id, amount):
        super().__init__(term_id, tr_id)
        self.org_id = org_id
        self.amount = amount

    def serialize(self):
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.org_id, self.amount))
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.org_id, self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """
        returns new PaymentTransaction exemplary with filled parameters
        :param data:
        :return:
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

    def serialize(self):
        self.length = super().get_length() + len(struct.pack(self.PACK_FORMAT, self.collector_id, self.amount))
        result = super().serialize(self.length, self.TYPE) + struct.pack(self.PACK_FORMAT, self.collector_id,
                                                                         self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """
        returns new PaymentTransaction exemplary with filled parameters
        :param data:
        :return:
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
        print('Serialized size {}'.format(sys.getsizeof(tr_serialized)))
        print('Deserialized info: {}'.format(tr.deserialize(tr_serialized)))
        print('Type: {}'.format(Transaction.get_type(tr_serialized)))
    print_transaction(PaymentTransaction(50, 1, 225, 8000))
    print_transaction(ServiceTransaction(50, 2, 'shutdown'))
    print_transaction(ServiceTransaction(50, 3, 'reload'))
    print_transaction(EncashmentTransaction(50, 4, 567, 20000))
    pass
