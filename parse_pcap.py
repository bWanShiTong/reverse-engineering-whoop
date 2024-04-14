from pyshark import FileCapture
from os import listdir


address = "F2:29:22:3E:72:78".lower()


def process_packet(packet):
    return packet.btatt.value.replace(':', '')


read_packages = []
write_packages = []

for file in listdir('logs/'):
    print(file)
    packages = FileCapture(f"logs/{file}")
    
    for packet in packages:
        try:
            read = packet.bthci_acl.dst_bd_addr.lower() == address
            write = packet.bthci_acl.src_bd_addr.lower() == address
                
            if not (read or write):
                continue

            packet = process_packet(packet)
            if packet == "0100":
                continue
                
            if write:
                write_packages.append(packet)
            else:
                read_packages.append(packet)
        except AttributeError:
            continue

    packages.close()

with open('data/captured-packages-read.txt', 'w') as file:
    file.write('\n'.join(read_packages).strip())


with open('data/captured-packages-write.txt', 'w') as file:
    file.write('\n'.join(write_packages).strip())