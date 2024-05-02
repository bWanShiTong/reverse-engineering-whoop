from pygatt import GATTToolBackend, BLEAddressType
from time import sleep
from dotenv import load_dotenv
from os import environ

load_dotenv()

address = environ['MAC_ADDR']

adapter = GATTToolBackend()
adapter.start()
device = adapter.connect(address, address_type=BLEAddressType.random)


def handle(data ,value):
    print(data, value)


device.subscribe('61080005-8d6d-82b8-614a-1c8cb0f8dcc6', callback=handle)


while True:
    device.char_write('61080002-8d6d-82b8-614a-1c8cb0f8dcc6', bytearray.fromhex('aa0800a8230e16001147c585'), wait_for_response=False)
    sleep(1)