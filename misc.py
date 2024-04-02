def little_endian_unix(buffer: str) -> int:
    buffer = [buffer[i:i+2] for i in range(0, len(buffer) , 2)][::-1]
    return int(''.join(buffer), 16)

def pretty_print(buffer: str, as_int: bool=False):
    buffer = [str(int(buffer[i:i+2], 16)) if as_int else buffer[i:i+2] for i in range(0, len(buffer), 2)]
    print(' '.join(buffer))

def decode_5c(package: str):
    header = package[:14]
    unix_s = package[14:20]
    separator = package[20:22]
    unix_e = package[22:30]
    crc_1 = package[30:32]
    crc_2 = package[32:34]

    s0 = package[34:36]
    s1 = package[36:38]
    s2 = package[38:40]
    s3 = package[40:42]

    assert s1 == "54"

    heart_rate = package[42:44] # ?

    s00 = package[44:58]

    padding = package[58:62]
    assert int(padding, 16) == 0, "Non zero padding"

    data0 = package[62:104]

    padding = package[104:106]
    assert int(padding, 16) == 0, "Non zero padding"

    data1 = package[106:170]

    padding = package[170:184]
    assert int(padding, 16) == 1
    checksum = package[184:]
    

def decode_1c(package: str):
    header = package[:14]
    unix = package[14:22]
    s0 = package[22:28]

    padding = package[28:34]
    assert int(padding, 16) == 0, "Non zero padding"

    s1 = package[34:40]
    padding = package[40:56]
    assert int(padding, 16) == 0, "Non zero padding"

    checksum = package[56:]

def decode_10(package: str):
    header = package[:14]
    unix = package[14:22]
    data = package[22:32]
    header = package[32:40]

def decode_2c(package: str):
    print(package)