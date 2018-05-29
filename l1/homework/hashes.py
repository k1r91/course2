import os
import hashlib


def hash_line(s, func):
    """
    >>> hash_line('I love Python', hashlib.sha1)
    '9233eac58259dd3a13d6c9c59f8001823b6b1fee'
    >>> hash_line('my name is', hashlib.md5)
    '01365b2bab5c481ab2880c798c1110d8'

    :param s: string to hash
    :param func: function to hash - hashlib.md5 for example
    :return: hash of string s
    """
    s = s.encode('cp1251')
    return func(s).hexdigest()


def main():
    writeable_data = []
    with open('need_hashes.csv', 'r', encoding='utf-8') as f:
        for line in f:
            data = line.split(';')
            if data[-1] in ['', os.linesep]:
                data[-1] = ''.join([hash_line(data[0], getattr(hashlib, data[1])), data[-1]])
            writeable_data.append(';'.join(data))
    with open('need_hashes.csv', 'w', encoding='utf-8') as f:
        for item in writeable_data:
            f.write(item)
if __name__ == '__main__':
    main()
