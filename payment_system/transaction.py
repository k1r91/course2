import datetime
import time


class SerializeException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


class Transaction:

    header = 0x7a7a     # 2 bytes for header
    TYPE_SZ = 8     # 1 byte for transaction type
    HEADER_SZ = 16
    LENGTH_SZ = 16
    YEAR_SZ = 7   # 7 bit for year
    MONTH_SZ = 4  # 4 bit for month
    DAY_SZ = 5    # 5 bit for day
    SEC_SZ = 24   # 3 bytes for seconds since midnight

    def __init__(self):
        self.date = None        # attribute defined in deserialize method
        self.length = None      # attribute defined in deserialize method
        self.type = None

    def get_type(self, data):
        cursor = self.HEADER_SZ + self.LENGTH_SZ + self.YEAR_SZ + self.MONTH_SZ + self.DAY_SZ + self.SEC_SZ
        return int(data[cursor:cursor+self.TYPE_SZ], 2)

    def get_datetime(self):
        """
        :return: current day in binary format according to protocol description ../l2/homework/README.MD
        * seconds since midnight
        """
        now = datetime.datetime.now()
        year = self.serialize_number(now.year, self.YEAR_SZ, is_year=True)
        month = self.serialize_number(now.month, self.MONTH_SZ)
        day = self.serialize_number(now.day, self.DAY_SZ)
        midnight = datetime.datetime.combine(now.date(), datetime.time())
        seconds = self.serialize_number((now - midnight).seconds, 24)
        return ''.join([year, month, day, seconds])

    @staticmethod
    def get_time(tseconds):
        hours = tseconds // 3600
        minutes = (tseconds - hours*3600) // 60
        seconds = tseconds - hours*3600 - minutes*60
        return hours, minutes, seconds

    @staticmethod
    def serialize_number(value, size, is_year=False):
        '''
        >>> serialize_number(24, 7)
        0011000
        >>> serialize_number(2017, 7, is_year=True)
        0010001

        :param self:
        :param value: number to serialize
        :param size: number of bits to pack value
        :param is_year: special logic to pack year in 7 bits: bin(current year - 2000)
        :return: string, binary representation of a value, packed in size bits
        '''
        if is_year:
            value -= 2000
        if value > 2 ** size:
            raise SerializeException('Can not serialize {}: {} bits is not enough'.format(value, size))
        res = str(bin(value))[2:]
        empty_bits = '0' * size
        diff = len(empty_bits) - len(res)
        if diff > 0:
            res = ''.join(['0'*diff, res])
        return res

    @property
    def serialized_header(self):
        return self.serialize_number(self.header, self.HEADER_SZ)

    @staticmethod
    def check_header(data):
        header = int(data[:Transaction.HEADER_SZ], 2)
        if header != Transaction.header:
            raise ValueError('Header is incorrect')

    @staticmethod
    def check_length(length, data):
        if length != len(data):
            raise ValueError('Length of packet is incorrect')


    @staticmethod
    def deserialize(data):
        """
        deserialize common deserializable data for all transaction
        :param data:
        :return:cursor - position to decode remaining bytecode data
        """
        result = {}
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        Transaction.check_header(data)
        cursor = Transaction.HEADER_SZ
        length = int(data[cursor:cursor+Transaction.LENGTH_SZ], 2)
        cursor += Transaction.LENGTH_SZ
        Transaction.check_length(length, data[cursor:])
        year = 2000 + int(data[cursor:cursor+Transaction.YEAR_SZ], 2)
        cursor += Transaction.YEAR_SZ
        month = int(data[cursor:cursor+Transaction.MONTH_SZ], 2)
        cursor += Transaction.MONTH_SZ
        day = int(data[cursor:cursor+Transaction.DAY_SZ], 2)
        cursor += Transaction.DAY_SZ
        total_seconds = int(data[cursor:cursor+Transaction.SEC_SZ], 2)
        cursor += Transaction.SEC_SZ
        hours, minutes, seconds = Transaction.get_time(total_seconds)
        date = datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)
        result['length'] = length
        result['date'] = date
        return result, cursor

    def __str__(self):
        return 'length={}, date={}'.format(self.length, self.date)


class ServiceTransaction(Transaction):
    data = {'power_on': 0x00,
            'reload': 0x01,
            'shutdown': 0x02,
            'activate_sensor': 0x03,
            'block': 0x04
            }
    ACTION_SZ = 8   # 1 byte to action
    TYPE = 0x00

    def __init__(self, action):
        super().__init__()
        self.action = self.data[action]

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.TYPE, self.TYPE_SZ),
                                    self.serialize_number(self.action, self.ACTION_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')

    @staticmethod
    def deserialize(data):
        """
        returns new ServiceTransaction exemplary with filled parameters
        :param data:
        :return:
        """
        result, cursor = Transaction.deserialize(data)
        ttype = int(data[cursor:cursor+ServiceTransaction.TYPE_SZ], 2)
        ServiceTransaction.check_type(ttype)
        cursor += ServiceTransaction.TYPE_SZ
        action = int(data[cursor:cursor+ServiceTransaction.ACTION_SZ], 2)
        res = ServiceTransaction(ServiceTransaction.get_key(ServiceTransaction.data, action))
        res.date = result['date']
        res.length = result['length']
        res.type = ttype
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

    ORG_ID_SZ = 32  # 4 bytes to organization id
    AMOUNT_SZ = 64  # 8 bytes to amount size
    TYPE = 0x01

    def __init__(self, org_id, amount):
        super().__init__()
        self.org_id = org_id
        self.amount = amount

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.TYPE, self.TYPE_SZ),
                                    self.serialize_number(self.org_id, self.ORG_ID_SZ),
                                    self.serialize_number(self.amount, self.AMOUNT_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')

    @staticmethod
    def deserialize(data):
        """

        :param data:
        :return:examplary of PaymentTranzaction class
        """
        result, cursor = Transaction.deserialize(data)
        ttype = int(data[cursor:cursor+Transaction.TYPE_SZ], 2)
        PaymentTransaction.check_type(ttype)
        cursor += Transaction.TYPE_SZ
        org_id = int(data[cursor:cursor+PaymentTransaction.ORG_ID_SZ], 2)
        cursor += PaymentTransaction.ORG_ID_SZ
        amount = int(data[cursor:cursor+PaymentTransaction.AMOUNT_SZ], 2)
        res = PaymentTransaction(org_id, amount)
        res.date = result['date']
        res.length = result['length']
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != PaymentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    def __str__(self):
        return 'Payment transaction: {}, org_id={}, amount={}'.format(super().__str__(), self.org_id, self.amount)


class EncashmentTransaction(Transaction):

    COLLECTOR_ID_SZ = 32    # 4 bytes to collector id
    AMOUNT_SZ = 64          # 8 bytes to encashment amount
    TYPE = 0x02

    def __init__(self, collector_id, amount):
        super().__init__()
        self.collector_id = collector_id
        self.amount = amount

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.TYPE, self.TYPE_SZ),
                                    self.serialize_number(self.collector_id, self.COLLECTOR_ID_SZ),
                                    self.serialize_number(self.amount, self.AMOUNT_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')

    @staticmethod
    def deserialize(data):
        """

        :param data:
        :return:examplary of PaymentTranzaction class
        """
        result, cursor = Transaction.deserialize(data)
        ttype = int(data[cursor:cursor + Transaction.TYPE_SZ], 2)
        EncashmentTransaction.check_type(ttype)
        cursor += Transaction.TYPE_SZ
        collector_id = int(data[cursor:cursor + EncashmentTransaction.COLLECTOR_ID_SZ], 2)
        cursor += PaymentTransaction.ORG_ID_SZ
        amount = int(data[cursor:cursor + EncashmentTransaction.AMOUNT_SZ], 2)
        res = EncashmentTransaction(collector_id, amount)
        res.date = result['date']
        res.length = result['length']
        return res

    @staticmethod
    def check_type(ttype):
        if ttype != EncashmentTransaction.TYPE:
            raise ValueError('Type is incorrect')

    def __str__(self):
        return 'Encashment transaction: {}, collector_id={}, amount={}'.format(super().__str__(), self.collector_id,
                                                                               self.amount)


if __name__ == '__main__':
    t = PaymentTransaction(225, 8000)
    serialized = t.serialize()
    print(t.deserialize(serialized))
    t2 = ServiceTransaction('shutdown')
    print(t2.serialize())
    print(t2.deserialize(t2.serialize()))
    t3 = ServiceTransaction('activate_sensor')
    print(t3.serialize())
    print(t3.deserialize(t3.serialize()))
    t4 = EncashmentTransaction(567, 20000)
    print(t4.serialize())
    print(t4.deserialize(t4.serialize()))
    pass
