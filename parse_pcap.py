from pyshark import FileCapture
from os import listdir
from datetime import datetime


address = "F2:29:22:3E:72:78".lower()

# bthci_acl.dst.bd_addr == F2:29:22:3E:72:78 && btatt

def process_packet(packet):
    return packet.btatt.value.replace(':', '')


read_packages = []
write_packages = []

for file in ["btsnoop_hci.log", "btsnoop_hci.log.last"]:
    print(file)
    packages = FileCapture(f"temp/{file}")
    
    for packet in packages:
        try:
            if packet.layers[-1].layer_name != "btatt":continue
            
            time = datetime.utcfromtimestamp(round(float(packet.frame_info.time_epoch)))
            if 6 <= time.hour:
                continue

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