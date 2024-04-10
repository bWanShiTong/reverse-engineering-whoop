from pyshark import FileCapture

file = "alarm-lot.log.last"
address = "F2:29:22:3E:72:78".lower()

packages = FileCapture(f"btsnoop_hci.log")

def process_packet(packet):
    return packet.btatt.value.replace(':', '')

with open('data/captured-packages.txt', 'a') as file:
    for packet in packages:
        try:
            if packet.bthci_acl.dst_bd_addr.lower() != address:
                continue

            # if packet.bthci_acl.src_bd_addr.lower() != address:
                # continue
            
            packet = process_packet(packet)
            if packet == "0100":
                continue
            
            file.write(f"{packet}\n")
            # print(packet)
        except AttributeError:
            continue