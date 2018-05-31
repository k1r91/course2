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
        self.type = None

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

    def check_header(self, data):
        header = int(data[:self.HEADER_SZ], 2)
        if header != self.header:
            raise ValueError('Header is incorrect')

    def check_length(self, length, data):
        if length != len(data):
            raise ValueError('Length of packet is incorrect')

    def check_type(self, ttype):
        if ttype != self.type:
            raise ValueError('Incorrect transaction type')

    def deserialize(self, data):
        data = data.decode('utf-8')
        self.check_header(data)
        cursor = self.HEADER_SZ
        length = int(data[cursor:cursor+self.LENGTH_SZ], 2)
        cursor += self.LENGTH_SZ
        self.check_length(length, data[cursor:])
        year = 2000 + int(data[cursor:cursor+self.YEAR_SZ], 2)
        cursor += self.YEAR_SZ
        month = int(data[cursor:cursor+self.MONTH_SZ], 2)
        cursor += self.MONTH_SZ
        day = int(data[cursor:cursor+self.DAY_SZ], 2)
        cursor += self.DAY_SZ
        total_seconds = int(data[cursor:cursor+self.SEC_SZ], 2)
        cursor += self.SEC_SZ
        hours, minutes, seconds = self.get_time(total_seconds)
        date = datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)
        return {'header': self.header, 'length': length, 'date': date}, cursor


class ServiceTransaction(Transaction):
    data = {'power_on': 0x00,
            'reload': 0x01,
            'shutdown': 0x02,
            'activate_sensor': 0x03,
            'block': 0x04
            }
    ACTION_SZ = 8   # 1 byte to action

    def __init__(self, action):
        self.type = 0x00
        self.action = self.data[action]

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.type, self.TYPE_SZ),
                                    self.serialize_number(self.collector_id_id, self.COLLECTOR_ID_SZ),
                                    self.serialize_number(self.amount, self.AMOUNT_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')


class PaymentTransaction(Transaction):

    ORG_ID_SZ = 32  # 4 bytes to organization id
    AMOUNT_SZ = 64  # 8 bytes to amount size

    def __init__(self, org_id, amount):
        self.type = 0x01
        self.org_id = org_id
        self.amount = amount

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.type, self.TYPE_SZ),
                                    self.serialize_number(self.org_id, self.ORG_ID_SZ),
                                    self.serialize_number(self.amount, self.AMOUNT_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')


    def deserialize(self, data):
        result, cursor = super().deserialize(data)
        ttype = int(data[cursor:cursor+self.TYPE_SZ], 2)
        self.check_type(ttype)
        cursor += self.TYPE_SZ
        org_id = int(data[cursor:cursor+self.ORG_ID_SZ], 2)
        cursor += self.ORG_ID_SZ
        amount = int(data[cursor:cursor+self.AMOUNT_SZ], 2)
        result['type'] = ttype
        result['org_id'] = org_id
        result['amount'] = amount
        return result


class EncashmentTransaction(Transaction):

    COLLECTOR_ID_SZ = 32    # 4 bytes to collector id
    AMOUNT_SZ = 64          # 8 bytes to encashment amount

    def __init__(self, collector_id, amount):
        self.type = 0x02
        self.collector_id = collector_id
        self.amount = amount

    def serialize(self):
        result = list()
        transaction_data = ''.join([self.serialize_number(self.type, self.TYPE_SZ),
                                    self.serialize_number(self.collector_id_id, self.COLLECTOR_ID_SZ),
                                    self.serialize_number(self.amount, self.AMOUNT_SZ)])
        self.length = len(self.get_datetime()) + len(transaction_data)
        serialized_length = self.serialize_number(self.length, self.LENGTH_SZ)
        result.append(self.serialized_header)
        result.append(serialized_length)
        result.append(self.get_datetime())
        result.append(transaction_data)
        return bytes(''.join(result), 'utf-8')


if __name__ == '__main__':
    t = PaymentTransaction(225, 8000)
    print(t.serialize())
    print(t.deserialize(t.serialize()))
    # print(t.serialize_number(24, 7))
    # print(t.get_datetime())
    # print(t.serialize_number(2100, 7, is_year=True))
    # Transaction.serialize_number(24, 5)
    pass