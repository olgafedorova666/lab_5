import logging

from . import boot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
)

with open("adams.dd", "rb") as file:
    parsed_boot = boot.Boot(file.read())
    print(parsed_boot.oem_name.as_ascii())
    print(int(parsed_boot.bytes_per_sector))
    print(parsed_boot.system_identifier.as_ascii())
    print(parsed_boot.volume_label.as_ascii())
    reserved_region = 0
    fat_region = reserved_region + int(parsed_boot.reserved_sectors_count)
    root_directory_region = fat_region + int(parsed_boot.table_count) * int(
        parsed_boot.table_size_16
    )
    data_region = root_directory_region + (
        (int(parsed_boot.root_entry_count) * 32) / int(parsed_boot.bytes_per_sector)
    )
    reserved_region_size = int(parsed_boot.reserved_sectors_count)
    fat_region_size = int(parsed_boot.table_count) * int(parsed_boot.table_size_16)
    root_directory_region_size = (int(parsed_boot.root_entry_count) * 32) / int(
        parsed_boot.bytes_per_sector
    )
    if parsed_boot.total_sectors_16 != b"\x00":
        total_sectors = parsed_boot.total_sectors_16
    else:
        total_sectors = parsed_boot.total_sectors_32

    data_region_size = (
        int(total_sectors)
        - int(reserved_region_size)
        - int(fat_region_size)
        - int(root_directory_region_size)
    )
    root_dir_entries_list = []
    for i in range(
        0, int(root_directory_region_size) * int(parsed_boot.bytes_per_sector), 32
    ):
        logging.debug(f"entry{i/32},start{root_directory_region * 512 + i}")
        file.seek(root_directory_region * 512 + i)
        entry_bytes = file.read(32)
        try:
            dir_entry = boot.RootDirEntry(entry_bytes)
            print(f"entry {i/32}, start {root_directory_region * 512 + i}")
            print(f"{dir_entry.file_name} - {dir_entry.attribute}")
            if dir_entry.attribute == "ARCHIVE":
                print(f"First cluster of a file {int(dir_entry.first_cluster_low)}")
                print(
                    f"First sector of a cluster {(data_region + (int(dir_entry.first_cluster_low)-2 * int(parsed_boot.sectors_per_cluster)))}"
                )
        except ValueError as e:
            pass
        root_dir_entries_list.append(dir_entry)
