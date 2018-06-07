import os
import hashlib
import magic
import pytest
import unittest


def glue(path_to_files, hash_file, result_filename):
    """
    >>> glue(os.path.join('files', 'file1'), 'parts.md5', 'result')
    243977

    :param path_to_files:
    :param hash_file:
    :param result_filename:
    :return:
    """
    ordered_files = []
    file_hashes = {}
    for file in os.scandir(path_to_files):
        if file.name != hash_file:
            with open(os.path.join(path_to_files, file.name), 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                file_hashes[file_hash] = file.name
    with open(os.path.join(path_to_files, hash_file), 'r', encoding='utf-8') as f:
        for line in f:
            hash_line = line.rstrip()
            ordered_files.append(file_hashes[hash_line])
    result_file_path = os.path.join(path_to_files, result_filename)
    with open(result_file_path, 'wb') as f:
        for file in ordered_files:
            with open(os.path.join(path_to_files, file), 'rb') as f_part:
                f.write(f_part.read())
    m = magic.open(magic.MAGIC_NONE)
    m.load()
    extension = '.' + m.file(result_file_path).split()[0].lower()
    os.rename(result_file_path, result_file_path + extension)

    return os.path.getsize(result_file_path + extension)


@pytest.mark.parametrize('path_to_files, hash_file, result_filename, expected',
                         [(os.path.join('files', 'file1'), 'parts.md5', 'result', 243977),
                          (os.path.join('files', 'file2'), 'parts.md5', 'result', 12224)
                          ])
def test_glue_file_size(path_to_files, hash_file, result_filename, expected):
    assert glue(path_to_files, hash_file, result_filename) == expected, 'Неверный размер файла'


class TestGlue(unittest.TestCase):
    def test_not_found_values(self):
        with self.assertRaises(FileNotFoundError):
            glue('', '', '')

if __name__ == '__main__':
    dir1 = os.path.join('files', 'file1')
    dir2 = os.path.join('files', 'file2')
    dir3 = 'for_split'
   #dir3 = os.path.join('for_split')
    glue(dir1, 'parts.md5', 'result')
    glue(dir2, 'parts.md5', 'result')
    glue(dir3, 'parts.md5', 'result')