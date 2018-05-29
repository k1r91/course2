import os
import hashlib
import random
import string
import unittest


def split_file(path_to_file, split_size):
    i = 0
    character_choice_list = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    with open(path_to_file, 'rb') as file:
        read_bytes = True
        dir_name = os.path.dirname(path_to_file)
        while read_bytes:
            read_bytes = file.read(split_size)
            small_file_name = ''.join(random.choice(character_choice_list) for _ in range(8))
            with open(os.path.join(dir_name, small_file_name), 'wb') as small_file:
                small_file.write(read_bytes)
                i += 1
            with open(os.path.join(dir_name, 'parts.md5'), 'a+', encoding='utf-8') as hash_file:
                hash_file.write(hashlib.md5(read_bytes).hexdigest() + os.linesep)
    return i


class TestSplit(unittest.TestCase):
    def test_file_numbers(self):
        assert split_file(os.path.join('for_split', 'cheatsheet.pdf'), 1024) == 13, 'Неверное число файлов'

if __name__ == '__main__':
    file_name = os.path.join('for_split', 'cheatsheet.pdf')
    print(split_file(file_name, 512))