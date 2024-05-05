from os import listdir, system

files = listdir('logs/')
files = [f'"logs/{file}"' for file in files]

system(f'mergecap -w output.log {" ".join(files)}')

# (bthci_acl.dst.bd_addr == F2:29:22:3E:72:78 || bthci_acl.src.bd_addr == F2:29:22:3E:72:78 ) && btatt.opcode.method == 0x11