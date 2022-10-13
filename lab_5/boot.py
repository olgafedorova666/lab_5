import string
import struct


class Data:
    def __init__(self, data) -> None:
        self.data = data

    def __int__(self) -> int:
        return int.from_bytes(self.data, byteorder='little')

    def as_ascii(self) -> string:
        return self.data.decode('ascii')

    def as_utf16(self) -> string:
        return self.data.decode('utf-16')

    def __hex__(self) -> string:
        return self.data.hex()

    def __bytes__(self) -> bytes:
        return self.data

    def __repr__(self) -> string:
        return self.data.decode('ascii')

    def __len__(self) -> int:
        return len(self.data)


class Boot:
    def __init__(self, data) -> None:
        self.bootjmp = Data(data[0:3])
        self.oem_name = Data(data[3:11])
        self.bytes_per_sector = Data(data[11:13])
        self.sectors_per_cluster = Data(data[13:14])
        self.reserved_sectors_count = Data(data[14:16])
        self.table_count = Data(data[16:17])
        self.root_entry_count = Data(data[17:19])
        self.total_sectors_16 = Data(data[19:21])
        self.media_type = Data(data[21:22])
        self.table_size_16 = Data(data[22:24])
        self.sectors_per_track = Data(data[24:26])
        self.head_side_count = Data(data[26:28])
        self.hidden_sector_count = Data(data[28:32])
        self.total_sectors_32 = Data(data[32:36])
        self.nt_flags_reserved = Data(data[36:38])
        self.signature = Data(data[38:39])
        self.volume_id = Data(data[39:43])
        self.volume_label = Data(data[43:54])
        self.system_identifier = Data(data[54:62])
        self.boot_code = Data(data[62:510])
        self.bootable_partition_signature = Data(data[510:512])


class RootDirEntry:
    def __init__(self, entry) -> None:
        if entry == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            raise ValueError('Empty entry')
        if entry[11:12] == b'\x01':
            self.attribute = 'READ_ONLY'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x02':
            self.attribute = 'HIDDEN'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x04':
            self.attribute = 'SYSTEM'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x08':
            self.attribute = 'VOLUME_ID'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x10':
            self.attribute = 'DIRECTORY'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x20':
            self.attribute = 'ARCHIVE'
            self.parse_standart(entry)
        elif entry[11:12] == b'\x0f':
            self.attribute = 'LONG_FILE_NAME'
            self.parse_lfn(entry)
        else:
            self.attribute = f'UNKNOWN_{entry[11:12]}'
            self.parse_standart(entry)
        pass

    def parse_lfn(self, entry) -> None:
        self.alloc_status = Data(entry[0:1])
        self.file_name_5 = Data(entry[1:11])
        self.long_entry_type = Data(entry[12:13])
        self.checksum = Data(entry[13:14])
        self.file_name_6 = Data(entry[14:26])
        self.file_name_2 = Data(entry[28:32])
        self.file_name = f'{self.file_name_5.as_utf16()}{self.file_name_6.as_utf16()}{self.file_name_2.as_utf16()}'
        pass

    def parse_standart(self, entry) -> None:
        self.file_name = Data(entry[0:11])
        self.nt_reserved = Data(entry[12:13])
        self.creation_time_s = Data(entry[13:14])
        self.creation_time_raw = Data(entry[14:16])
        self.creation_date_raw = Data(entry[16:18])
        self.last_access_date_raw = Data(entry[18:20])
        self.first_cluster_high = Data(entry[20:22])
        self.modification_time_raw = Data(entry[22:24])
        self.modification_date_raw = Data(entry[24:26])
        self.first_cluster_low = Data(entry[26:28])
        self.file_size = Data(entry[28:32])
        self.creation_time = self.decode_fat_time(self.creation_time_raw)
        self.creation_date = self.decode_fat_date(self.creation_date_raw)
        self.last_access_date = self.decode_fat_date(self.last_access_date_raw)
        self.modification_time = self.decode_fat_time(self.modification_time_raw)
        self.modification_date = self.decode_fat_date(self.modification_date_raw)

    def as_unsigned(self, bs, endian='<'):
        unsigned_format = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
        if len(bs.__bytes__()) <= 0 or len(bs.__bytes__()) > 8:
            raise ValueError()
        fill = '\x00'
        while len(bs.__bytes__()) not in unsigned_format:
            bs = bs.__bytes__() + fill
        result = struct.unpack(endian + unsigned_format[len(bs.__bytes__())], bs.__bytes__())[0]
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
