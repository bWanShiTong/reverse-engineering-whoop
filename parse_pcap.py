from pyshark import FileCapture
from os import listdir, remove, environ
from datetime import datetime
from dotenv import load_dotenv
from json import dumps

load_dotenv()

address = environ['MAC_ADDR'].upper()

def process_packet(packet):
    return packet.btatt.value.replace(':', '')


read_packages = {}
write_packages = {}

opcodes = {}
for file in listdir('logs/'):
    # if file != "2024-05-01T07:03:52.log":continue

    packages = FileCapture(f"logs/{file}")

    total_packages = len(read_packages) + len(write_packages)
    
    for packet in packages:
        try:
            if packet.layers[-1].layer_name != "btatt":continue
            
            time = datetime.utcfromtimestamp(round(float(packet.frame_info.time_epoch)))
            # if time.month != 5 or time.hour != 6 or time.minute < 40:
            #     continue
            
            # print(time)

            write = packet.bthci_acl.dst_bd_addr.upper() == address
            read = packet.bthci_acl.src_bd_addr.upper() == address

            if not (read or write):
                continue
            
            p = process_packet(packet)
            if packet.btatt.opcode == '0x1d':
                continue
                
            # if packet.btatt.opcode != '0x1b':
            #     continue

            # print(packet)
            # exit()
            opcodes[packet.btatt.opcode] = opcodes[packet.btatt.opcode] + 1 if opcodes.get(packet.btatt.opcode) else 1
            if write:
                write_packages[p] = None
            else:
                read_packages[p] = None
        except AttributeError:
            continue

    packages.close()
    # if len(read_packages) + len(write_packages) == total_packages:
    #     remove(f'logs/{file}')
        

with open('data/captured-packages-read.txt', 'w') as file:
    file.write('\n'.join(read_packages.keys()).strip())


with open('data/captured-packages-write.txt', 'w') as file:
    file.write('\n'.join(write_packages.keys()).strip())


print(dumps(opcodes, indent=4))