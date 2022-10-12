from pkg_resources import empty_provider
from . import boot

with open('adams.dd', 'rb') as file:
    parsed_boot = boot.Boot(file.read())
    print(parsed_boot.oem_name.decode('ascii'))
    print(int.from_bytes(parsed_boot.bytes_per_sector, byteorder='little'))
    print(parsed_boot.system_identifier.decode('ascii'))
    print(parsed_boot.volume_label.decode('ascii'))
    rootDirSectors = int(int.from_bytes(parsed_boot.root_entry_count, byteorder='little')
                         * 32) / int.from_bytes(parsed_boot.bytes_per_sector, byteorder='little')
    dataSec = int.from_bytes(parsed_boot.total_sectors_16, byteorder='little') - (int.from_bytes(parsed_boot.reserved_sectors_count, byteorder='little') + (
        int.from_bytes(parsed_boot.table_count, byteorder='little') * int.from_bytes(parsed_boot.table_size_16, byteorder='little')) + rootDirSectors)
    print(dataSec)
    root_dir_offset = int.from_bytes(parsed_boot.table_size_16, byteorder='little') * \
        2 * int.from_bytes(parsed_boot.bytes_per_sector,
                           byteorder='little') + 512
    root_dir_entries_list = []
    print(root_dir_offset+int(rootDirSectors) * int.from_bytes(parsed_boot.bytes_per_sector, byteorder='little'))
    for i in range(0, int(rootDirSectors) * int.from_bytes(parsed_boot.bytes_per_sector, byteorder='little'), 32):
        file.seek(root_dir_offset+i)
        entry_bytes = file.read(32)
        try:
            dir_entry = boot.RootDirEntry(entry_bytes)
            print(dir_entry.file_name)
            root_dir_entries_list.append(dir_entry)
        except ValueError:
            pass

