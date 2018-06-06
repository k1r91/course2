import datetime
import struct


sformat = 'H'


def pack_date(year_sz, month_sz, day_sz):
    now = datetime.datetime.now()
    year = now.year - 2000
    print(year)
    day = now.day
    month = now.month
    print(year, month, day)
    year_str = str(bin(year)[2:]).zfill(7)
    print(year_str)
    month_str = str(bin(month)[2:]).zfill(4)
    print(month_str)
    day_str = str(bin(day)[2:]).zfill(5)
    print(day_str)
    date_code_num = int(''.join([year_str, month_str, day_str]), 2)
    print(date_code_num)
    result = struct.pack(sformat, date_code_num)
    print(year_str+month_str+day_str)
    return result

def unpack_date(year_sz, month_sz, day_sz, packed_date):
    unpack = struct.unpack(sformat, packed_date)[0]
    raw_str = str(bin(unpack))[2:].zfill(year_sz+month_sz+day_sz)
    print(raw_str)
    # print(str(bin(unpack))[2:].zfill(year_sz+month_sz+day_sz))
    year = int(raw_str[:year_sz], 2)
    month = int(raw_str[year_sz: year_sz+month_sz], 2)
    day = int(raw_str[year_sz+month_sz: year_sz+month_sz+day_sz], 2)
    return year, month, day

packed = pack_date(7, 4, 5)
print(unpack_date(7, 4, 5, packed))