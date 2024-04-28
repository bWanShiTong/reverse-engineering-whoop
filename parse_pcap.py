from pyshark import FileCapture
from os import listdir, remove, environ
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

address = environ['MAC_ADDR']

def process_packet(packet):
    return packet.btatt.value.replace(':', '')


read_packages = {}
write_packages = {}

for file in listdir('logs/'):
    print(file)
    packages = FileCapture(f"logs/{file}")

    total_packages = len(read_packages) + len(write_packages)
    
    for packet in packages:
        try:
            if packet.layers[-1].layer_name != "btatt":continue
            
            time = datetime.utcfromtimestamp(round(float(packet.frame_info.time_epoch)))

            read = packet.bthci_acl.dst_bd_addr.lower() == address
            write = packet.bthci_acl.src_bd_addr.lower() == address

            if not (read or write):
                continue

            packet = process_packet(packet)
                
            if write:
                write_packages[packet] = None
            else:
                read_packages[packet] = None
        except AttributeError:
            continue

    packages.close()
    print(len(read_packages) + len(write_packages), total_packages)
    if len(read_packages) + len(write_packages) == total_packages:
        remove(f'logs/{file}')
        

with open('data/captured-packages-read.txt', 'w') as file:
    file.write('\n'.join(read_packages.keys()).strip())


with open('data/captured-packages-write.txt', 'w') as file:
    file.write('\n'.join(write_packages.keys()).strip())