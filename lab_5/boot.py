import struct

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
        self.nt_flags_resrved = data[36:38]
        self.signature = data[38:39]
        self.volume_id = data[39:43]
        self.volume_label = data[43:54]
        self.system_identifier = data[54:62]
        self.boot_code = data[62:510]
        self.bootable_partition_signature = data[510:512]

class RootDirEntry:
    def __init__(self, entry) -> None:
        if entry == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            raise ValueError
        if entry[11:12] == b'\01':
            self.attribute = 'READ_ONLY'
            self.parse_standart(entry)
        elif entry[11:12] == b'\02':
            self.attribute = 'HIDDEN'
            self.parse_standart(entry)
        elif entry[11:12] == b'\04':
            self.attribute = 'SYSTEM'
            self.parse_standart(entry)
        elif entry[11:12] == b'\08':
            self.attribute = 'VOLUME_ID'
            self.parse_standart(entry)
        elif entry[11:12] == b'\10':
            self.attribute = 'DIRECTORY'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x20':
            self.attribute = 'ARCHIVE'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x0f':
            self.attribute = 'LONG_FILE_NAME'
            self.parse_standart(entry)
        else: 
            self.attribute = f'UNKNOWN_{entry[11:12]}'
            self.parse_standart(entry)
        pass

    def parse_standart(self, entry) -> None:
        self.file_name = entry[0:11]
        self.nt_reserved = entry[12:13]
        self.creation_time_s = entry[13:14]
        self.creation_time_raw = entry[14:16]
        self.creation_date_raw = entry[16:18]
        self.last_access_date_raw = entry[18:20]
        self.first_cluster_high = entry[20:22]
        self.modification_time_raw = entry[22:24]
        self.modification_date_raw = entry[24:26]
        self.first_cluster_low = entry[26:28]
        self.file_size = entry[28:32]
        
        self.creation_time = self.decode_fat_time(self.creation_time_raw
        )
        self.creation_date = self.decode_fat_date(self.creation_date_raw
        )
        self.last_access_date = self.decode_fat_date(self.last_access_date_raw)
        self.modification_time = self.decode_fat_time(self.modification_time_raw)
        self.modification_date = self.decode_fat_date(self.modification_date_raw
        )


    def as_unsigned(self, bs, endian='<'):
        unsigned_format = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
        if len(bs) <= 0 or len(bs) > 8:
            raise ValueError()
        fill = '\x00'
        while len(bs) not in unsigned_format:
            bs = bs + fill
        result = struct.unpack(endian + unsigned_format[len(bs)], bs)[0]
        return result

    def decode_fat_time(self, time_bytes, tenths=0, tz='EDT'):
        v = self.as_unsigned(time_bytes)
        second = int(int(0x1F & v) * 2)
        if tenths > 100:
            second += 1
        minute = (0x7E0 & v) >> 5
        hour = (0xF800 & v) >> 11
        return '{:02}:{:02}:{:02} ({})'.format(hour, minute, second, tz)

    def decode_fat_date(self, date_bytes):
        v = self.as_unsigned(date_bytes)
        day = 0x1F & v
        month = (0x1E0 & v) >> 5
        year = ((0xFE00 & v) >> 9) + 1980
        return '{}-{:02}-{:02}'.format(year, month, day)
