from curses.ascii import NUL
import math
from . import boot

with open('adams.dd', 'rb') as file:
    parsed_boot = boot.Boot(file.read())
    print(parsed_boot.oem_name.as_ascii())
    print(int(parsed_boot.bytes_per_sector))
    print(parsed_boot.system_identifier.as_ascii())
    print(parsed_boot.volume_label.as_ascii())
    rootDirSectors = int(parsed_boot.root_entry_count) * 32 / int(parsed_boot.bytes_per_sector)
    dataSec = int(parsed_boot.total_sectors_16) - (int(parsed_boot.reserved_sectors_count) + int(parsed_boot.table_count) * int(parsed_boot.table_size_16))
    print('dataSec:', dataSec)
    root_dir_offset = int(parsed_boot.table_size_16) * int(parsed_boot.table_count) * int(parsed_boot.bytes_per_sector) + 512
    
    
    root_Starting_Sector = int(parsed_boot.reserved_sectors_count) + int(parsed_boot.table_count)*int(parsed_boot.table_size_16)
    root_Starting_Byte = root_Starting_Sector * int(parsed_boot.bytes_per_sector)
    print('root_Starting_Byte:', root_Starting_Byte)
    root_dir_entries_list = []
    root_size = int(parsed_boot.root_entry_count) * 32 / int(parsed_boot.bytes_per_sector)
    root_size_byte = root_size * int(parsed_boot.bytes_per_sector)
    print('root_dir_offset:', root_dir_offset)
    

    data_start_1 = 512 * int(parsed_boot.reserved_sectors_count) + int(parsed_boot.table_size_16) * int(parsed_boot.table_count) + root_size_byte
    print('data_start_1:', data_start_1)
    data_start = root_Starting_Sector + root_size
    print('data_start:', data_start)
    data_start_byte = root_dir_offset + root_size_byte
    print('data_start_byte:', data_start_byte, data_start)
    for i in range(0, (int(root_size) + 1 ) * int(parsed_boot.bytes_per_sector), 32):
        #file.seek(root_dir_offset + i)
        file.seek(root_Starting_Byte + i)
        entry_bytes = file.read(32)
        try:
            dir_entry = boot.RootDirEntry(entry_bytes)
            print(f'{dir_entry.file_name} - {dir_entry.attribute}')
            if dir_entry.attribute == ('ARCHIVE' or 'LONG_FILE_NAME'):
                print(f'{int(dir_entry.first_cluster_low)}')
                file_start = int(dir_entry.first_cluster_low) * 1024 + data_start_byte
                file_end = int(dir_entry.file_size) + file_start
                print(file_start, file_end)
        except ValueError as e:
            pass
        root_dir_entries_list.append(dir_entry)
