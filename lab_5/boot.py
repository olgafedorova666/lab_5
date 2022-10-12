class Boot:
    def __init__(self, data) -> None:
        self.booyjmp = data[0:3]
        self.oem_name = data[3:11]
        self.bytes_per_sector = data[11:13]
        self.sectors_per_cluster = data[13:14]
        self.reserved_sectors_count = data[14:16]
        self.table_count = data[16:17]
        self.root_entry_count = data[17:19]
        self.total_sectors_16 = data[19:21]
        self.media_type = data[21:22]
        self.table_size_16 = data[22:24]
        self.sectors_per_track = data[24:26]
        self.head_side_count = data[26:28]
        self.hidden_sector_count = data[28:32]
        self.total_sectors_32 = data[32:36]
        self.nt_flags_resrved = data[37:38]
        self.signature = data[38:39]
        self.volume_id = data[39:43]
        self.volume_label = data[43:54]
        self.system_identifier = data[54:62]
        self.boot_code = data[62:510]
        self.bootable_partition_signature = data[510:512]

    def __repr__(self) -> str:
        pass