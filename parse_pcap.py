from pyshark import FileCapture
from os import listdir, remove, environ
from datetime import datetime
from dotenv import load_dotenv
from json import dumps

load_dotenv()

address = environ['MAC_ADDR'].upper()

def process_packet(packet):
    return packet.btatt.value.replace(':', '')


read_packages = []
write_packages = []

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
            if packet.btatt.opcode == '0x1d' or packet.btatt.opcode == '0x12' or len(p) <= 4:
                continue
                

            bytes_length = int(p[2:4], 16)
            if bytes_length == 0:
                continue

            length_in_bytes = len(p[4:]) / 2 - 2
            if length_in_bytes != bytes_length:
                continue
            # if packet.btatt.opcode != '0x1b':
            #     continue

            # print(packet)
            # exit()
            opcodes[packet.btatt.opcode] = opcodes[packet.btatt.opcode] + 1 if opcodes.get(packet.btatt.opcode) else 1
            if write:
                if isinstance(write_packages, list):
                    write_packages.append(p)
                elif isinstance(write_packages, dict):
                    write_packages[p] = None
                else:
                    raise "Wong"
            else:
                if isinstance(read_packages, list):
                    read_packages.append(p)
                elif isinstance(read_packages, dict):
                    read_packages[p] = None
                else:
                    raise "Wong"
        except AttributeError:
            continue

    packages.close()
    # if len(read_packages) + len(write_packages) == total_packages:
    #     remove(f'logs/{file}')
        

with open('data/captured-packages-read.txt', 'w') as file:
    if isinstance(read_packages, list):
        file.write('\n'.join(read_packages).strip())
    elif isinstance(read_packages, dict):
        file.write('\n'.join(read_packages.keys()).strip())
    else:
        raise "Wong"


with open('data/captured-packages-write.txt', 'w') as file:
    if isinstance(write_packages, list):
        file.write('\n'.join(write_packages).strip())
    elif isinstance(write_packages, dict):
        file.write('\n'.join(write_packages.keys()).strip())
    else:
        raise "Wong"


print(dumps(opcodes, indent=4))