from pyshark import FileCapture

file = "btsnoop_hci copy.log"
address = "F2:29:22:3E:72:78".lower()

packages = FileCapture(file)

def process_packet(packet):
    return packet.btatt.value.replace(':', '')

with open('captured-packages.txt', 'w') as file:
    for packet in packages:
        try:
            if packet.bthci_acl.dst_bd_addr.lower() != address:
                continue

            packet = process_packet(packet)
            if packet == "0100":
                continue
            
            file.write(f"{packet}\n")
        except AttributeError:
            continue