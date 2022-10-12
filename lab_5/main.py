from lib2to3.refactor import get_all_fix_names
import struct


def as_le_unsigned(b):
    table = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    return struct.unpack('<' + table[len(b)], b)[0]


def get_sector_size(fs_bytes):
    return as_le_unsigned(fs_bytes[11:13])


def get_cluster_size(fs_bytes):
    return as_le_unsigned(fs_bytes[13:14]) * get_sector_size(fs_bytes)


def get_reserved_area_size(fs_bytes):
    return as_le_unsigned(fs_bytes[14:16]) * get_sector_size(fs_bytes)


def get_fat_size(fs_bytes):
    return as_le_unsigned(fs_bytes[22:24]) * get_sector_size(fs_bytes)


def get_fat0(fs_bytes):
    start = get_reserved_area_size(fs_bytes)
    length = get_fat_size(fs_bytes)
    return fs_bytes[start:start + length]


def get_number_of_fats(fs_bytes):
    return as_le_unsigned(fs_bytes[16:17])


def get_max_root_directory_entries(fs_bytes):
    return as_le_unsigned(fs_bytes[17:19])


def get_root_directory_area(fs_bytes):
    start = get_reserved_area_size(
        fs_bytes) + get_number_of_fats(fs_bytes) * get_fat_size(fs_bytes)
    length = get_max_root_directory_entries(fs_bytes) * 32  # 32 bytes / entry
    return fs_bytes[start:start + length]


def get_sector_count(fs_bytes):
    return max(as_le_unsigned(fs_bytes[19:21]), as_le_unsigned(fs_bytes[32:36]))


def get_cluster_area(fs_bytes):
    fs_size = get_sector_count(fs_bytes) * get_sector_size(fs_bytes)
    start = get_reserved_area_size(fs_bytes) + get_number_of_fats(
        fs_bytes) * get_fat_size(fs_bytes) + get_max_root_directory_entries(fs_bytes) * 32
    number_of_clusters = (fs_size - start) // get_cluster_size(fs_bytes)
    length = number_of_clusters * get_cluster_size(fs_bytes)
    return fs_bytes[start:start + length]


def get_filename(dirent):
    return dirent[0:8].decode('ascii').strip() + '.' + dirent[8:11].decode('ascii')


def get_first_cluster(dirent):
    return as_le_unsigned(dirent[26:28])


def get_filesize(dirent):
    return as_le_unsigned(dirent[28:32])


def get_cluster_numbers(cluster_number, fat_bytes, cluster_size):
    if cluster_number >= as_le_unsigned(b'\xf8\xff'):  # handle edge case first
        return [cluster_number]
    result = []
    while cluster_number < as_le_unsigned(b'\xf8\xff'):  # should be < not >=
        result.append(cluster_number)
        # offset is * 2 bytes per cluster, not cluster size in bytes
        offset = cluster_number * 2
        cluster_number = as_le_unsigned(fat_bytes[offset:offset + 2])
        return result


def main():
    with open('adams.dd', 'rb') as f:
        data = f.read()
    print('sector size:', get_sector_size(data))
    print('cluster size:', get_cluster_size(data))
    print('reserved area size:', get_reserved_area_size(data))
    print('FAT size:', get_fat_size(data))
    print('max root entries:', get_max_root_directory_entries(data))
    print('number of FATs:', get_number_of_fats(data))
    print('sector count:', get_sector_count(data))
   
    print('1. fat_size:', get_fat_size(data))
    print('2. reserved_area_size:', get_reserved_area_size(data))
    print('3. all_fix_names:', get_all_fix_names)

    root_directory_entries = get_root_directory_area(data)
    dirent = root_directory_entries[32 * 3: 32 * 4]
    print('filename:', get_filename(dirent))
    print('first cluster:', get_first_cluster(dirent))
    print('file size:', get_filesize(dirent))
    print('cluster numbers:', get_cluster_numbers(get_first_cluster(dirent),
                                                  get_fat0(data), get_cluster_size(data)))


if __name__ == '__main__':
    main()
