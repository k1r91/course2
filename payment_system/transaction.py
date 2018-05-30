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
    HEADER_SZ = 16
    LENGTH_SZ = 16
    YEAR_SZ = 7   # 7 bit for year
    MONTH_SZ = 4  # 4 bit for month
    DAY_SZ = 5    # 5 bit for day
    SEC_SZ = 24   # 3 bytes for seconds since midnight

    def get_length(self):
        """
        >>> self.get_length()
        40

        :return: length of current transaction data (actually length of datetime field)
        """
        return len(self.get_datetime())

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


class ServiceTransaction(Transaction):
    data = {'power_on': 0x00,
            'reload': 0x01,
            'shutdown': 0x02,
            'activate_sensor': 0x03,
            'block': 0x04
            }

    def __init__(self, action):
        self.type = 0x00
        self.action = self.data[action]

    def serialize(self):
        pass


class PaymentTransaction(Transaction):

    def __init__(self, org_id, amount):
        self.type = 0x01
        self.org_id = org_id
        self.amount = amount


class EncashmentTransaction(Transaction):

    def __init__(self, collector_id, amount):
        self.type = 0x02
        self.collector_id = collector_id
        self.amount = amount


if __name__ == '__main__':
    # t = Transaction()
    # print(t.serialize_number(24, 7))
    # print(t.get_datetime())
    # print(t.serialize_number(2100, 7, is_year=True))
    # Transaction.serialize_number(24, 5)
    pass