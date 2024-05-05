from pygatt import GATTToolBackend, BLEAddressType
from time import sleep
from dotenv import load_dotenv
from os import environ
from misc import *

load_dotenv()

address = environ['MAC_ADDR']

adapter = GATTToolBackend(hci_device='hci1')
adapter.start()
device = adapter.connect(address, address_type=BLEAddressType.random, timeout=10.0)


def handle(data ,value):
    data = ''.join([format(x, '02x') for x in value])
    header = data[0:4]

    if header == "aa5c":
        decode_5c(data)




# device.subscribe('61080003-8d6d-82b8-614a-1c8cb0f8dcc6', callback=handle)
# device.subscribe('61080005-8d6d-82b8-614a-1c8cb0f8dcc6', callback=handle)


# while True:
#     # device.char_write('61080002-8d6d-82b8-614a-1c8cb0f8dcc6', bytearray.fromhex('aa0800a8230e16001147c585'), wait_for_response=False)
#     sleep(1)
#     # pass

device.char_write('61080002-8d6d-82b8-614a-1c8cb0f8dcc6', bytearray.fromhex('aa0800a8230e16001147c585'), wait_for_response=True)