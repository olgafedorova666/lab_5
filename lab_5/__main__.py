from . import boot

with open('adams.dd', 'rb') as file: 
    parsed_boot = boot.Boot(file.read())
    print(parsed_boot.oem_name.decode('ascii'))
    print(int.from_bytes(parsed_boot.bytes_per_sector, byteorder='little'))
    print(parsed_boot.system_identifier.decode('ascii'))
    print(parsed_boot.volume_label.decode('ascii'))