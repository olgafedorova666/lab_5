import math
from . import boot

with open('adams.dd', 'rb') as file:
    parsed_boot = boot.Boot(file.read())
    print(parsed_boot.oem_name.as_ascii())
    print(int(parsed_boot.bytes_per_sector))
    print(parsed_boot.system_identifier.as_ascii())
    print(parsed_boot.volume_label.as_ascii())
    rootDirSectors = int(parsed_boot.root_entry_count) * 32 / int(parsed_boot.bytes_per_sector)
    dataSec = int(parsed_boot.total_sectors_16) - int(parsed_boot.reserved_sectors_count) + int(parsed_boot.table_count) * int(parsed_boot.table_size_16)
    root_dir_offset = int(parsed_boot.table_size_16) * 2 * int(parsed_boot.bytes_per_sector) + 512
    root_dir_entries_list = []
    root_size = int(parsed_boot.root_entry_count) * 32 / int(parsed_boot.bytes_per_sector)

    data_start = 512 * int(parsed_boot.reserved_sectors_count) + int(parsed_boot.table_size_16) * int(parsed_boot.table_count) + root_size
    for i in range(0, int(rootDirSectors) * int(parsed_boot.bytes_per_sector), 32):
        file.seek(root_dir_offset + i)
        entry_bytes = file.read(32)
        try:
            dir_entry = boot.RootDirEntry(entry_bytes)
            print(f'{dir_entry.file_name} - {dir_entry.attribute}')
            if dir_entry.attribute == 'ARCHIVE':
                print(f'{int(dir_entry.first_cluster_low)}')
        except ValueError as e:
            pass
        root_dir_entries_list.append(dir_entry)
