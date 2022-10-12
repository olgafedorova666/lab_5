from distutils.debug import DEBUG
import logging

logging.basicConfig(level=DEBUG)

data = b'Hello World!'
print(len(data))
with open('adams.dd', 'r+b') as file:
    sector_size = 512
    offset = 73 * sector_size
    file.seek(offset)
    while file.read(len(data)) 
    print(offset)
#with open('adams.dd', 'wb') as file:
#    file.seek()
#    file.write(data)
