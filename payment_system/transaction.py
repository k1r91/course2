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
    PACK_FORMAT = 'HBBBBIB'

    def __init__(self):
        self.date = None        # attribute defined in deserialize method
        self.length = None      # attribute defined in deserialize method
        self.type = None

    @staticmethod
    def get_type(data):
        data = struct.unpack(Transaction.PACK_FORMAT, data[:13])    # 13 is expected size of data to unpack according
                                                                    # to PACK FORMAT
        return data[-1]

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
    def get_time(tseconds):
        hours = tseconds // 3600
        minutes = (tseconds - hours*3600) // 60
        seconds = tseconds - hours*3600 - minutes*60
        return hours, minutes, seconds

    @staticmethod
    def check_header(header):
        if header != Transaction.header:
            raise ValueError('Header is incorrect!')

    def __str__(self):
        return 'length={}, date={}'.format(self.length, self.date)


class ServiceTransaction(Transaction):
    data = {'power_on': 0x00,
            'reload': 0x01,
            'shutdown': 0x02,
            'activate_sensor': 0x03,
            'block': 0x04
            }
    TYPE = 0x00
    PACK_FORMAT = Transaction.PACK_FORMAT + 'B'

    def __init__(self, action):
        super().__init__()
        self.action = self.data[action]

    def serialize(self):
        now = datetime.datetime.now()
        year = now.year - 2000
        seconds = Transaction.seconds_since_midnight()
        self.length = len(struct.pack(self.PACK_FORMAT[2:], year, now.month, now.day,  seconds, self.TYPE, self.action))
        result = struct.pack(self.PACK_FORMAT, self.header, self.length, year, now.month, now.day,
                             seconds, self.TYPE, self.action)
        return result

    @staticmethod
    def deserialize(data):
        """
        returns new ServiceTransaction exemplary with filled parameters
        :param data:
        :return:
        """
        data = struct.unpack(ServiceTransaction.PACK_FORMAT, data)
        header = data[0]
        Transaction.check_header(header)
        ttype = data[6]
        ServiceTransaction.check_type(ttype)
        action = ServiceTransaction.get_key(ServiceTransaction.data, data[7])
        res = ServiceTransaction(action)
        res.length = data[1]
        hours, minutes, seconds = Transaction.get_time(data[5])
        res.date = datetime.datetime(year=2000+data[2], month=data[3], day=data[4], hour=hours, minute=minutes,
                                     second=seconds)
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


class PaymentTransaction(Transaction):
    TYPE = 0x01
    PACK_FORMAT = Transaction.PACK_FORMAT + 'IQ'

    def __init__(self, org_id, amount):
        super().__init__()
        self.org_id = org_id
        self.amount = amount

    def serialize(self):
        """
        Serialize for payment transaction
        :return: 
        """
        now = datetime.datetime.now()
        year = now.year - 2000
        seconds = Transaction.seconds_since_midnight()
        self.length = len(struct.pack(self.PACK_FORMAT[2:], year, now.month, now.day, seconds, self.TYPE,
                                      self.org_id, self.amount))
        result = struct.pack(self.PACK_FORMAT, self.header, self.length, year, now.month, now.day,
                             seconds, self.TYPE, self.org_id, self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """

        :param data:
        :return:examplary of PaymentTransaction class
        """
        data = struct.unpack(PaymentTransaction.PACK_FORMAT, data)
        header = data[0]
        Transaction.check_header(header)
        ttype = data[6]
        PaymentTransaction.check_type(ttype)
        org_id, amount = data[7], data[8]
        res = PaymentTransaction(org_id, amount)
        res.length = data[1]
        hours, minutes, seconds = Transaction.get_time(data[5])
        res.date = datetime.datetime(year=2000 + data[2], month=data[3], day=data[4], hour=hours, minute=minutes,
                                     second=seconds)
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != PaymentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    def __str__(self):
        return 'Payment transaction: {}, org_id={}, amount={}'.format(super().__str__(), self.org_id, self.amount)


class EncashmentTransaction(Transaction):

    PACK_FORMAT = Transaction.PACK_FORMAT + 'IQ'
    TYPE = 0x02

    def __init__(self, collector_id, amount):
        super().__init__()
        self.collector_id = collector_id
        self.amount = amount

    def serialize(self):
        """
        Serialize for payment transaction
        :return: 
        """
        now = datetime.datetime.now()
        year = now.year - 2000
        seconds = Transaction.seconds_since_midnight()
        self.length = len(struct.pack(self.PACK_FORMAT[2:], year, now.month, now.day, seconds, self.TYPE,
                                      self.collector_id, self.amount))
        result = struct.pack(self.PACK_FORMAT, self.header, self.length, year, now.month, now.day,
                             seconds, self.TYPE, self.collector_id, self.amount)
        return result

    @staticmethod
    def deserialize(data):
        """

        :param data:
        :return:examplary of PaymentTransaction class
        """
        data = struct.unpack(PaymentTransaction.PACK_FORMAT, data)
        header = data[0]
        Transaction.check_header(header)
        ttype = data[6]
        EncashmentTransaction.check_type(ttype)
        collector_id, amount = data[7], data[8]
        res = EncashmentTransaction(collector_id, amount)
        res.length = data[1]
        hours, minutes, seconds = Transaction.get_time(data[5])
        res.date = datetime.datetime(year=2000 + data[2], month=data[3], day=data[4], hour=hours, minute=minutes,
                                     second=seconds)
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != EncashmentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    def __str__(self):
        return 'Encashment transaction: {}, collector_id={}, amount={}'.format(super().__str__(), self.collector_id,
                                                                               self.amount)


if __name__ == '__main__':
    def print_transaction(tr):
        tr_serialized = tr.serialize()
        print('Serialized transaction: {}'.format(tr_serialized))
        print('Serialized size {}'.format(sys.getsizeof(tr_serialized)))
        print('Deserialized info: {}'.format(tr.deserialize(tr_serialized)))
        print(Transaction.get_type(tr_serialized))
    print_transaction(PaymentTransaction(225, 8000))
    print_transaction(ServiceTransaction('shutdown'))
    print_transaction(ServiceTransaction('reload'))
    print_transaction(EncashmentTransaction(567, 20000))
    pass
