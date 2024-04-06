def little_endian(buffer: str) -> int:
    return int.from_bytes(bytearray.fromhex(buffer), 'little')

def pretty_print(buffer: str, as_int: bool=False):
    buffer = [str(int(buffer[i:i+2], 16)).ljust(4) if as_int else buffer[i:i+2] for i in range(0, len(buffer), 2)]
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

    count = int(package[44:46], 16)
    s00 = bytearray.fromhex(package[46:62]) # RR?
    rr = []
    for i in range(0, count, 2):
        buf = s00[i:i+2]
        rr.append(int.from_bytes(buf, 'little'))

    data0 = package[62:104]

    padding = package[104:106]
    assert int(padding, 16) == 0, "Non zero padding"

    data1 = package[106:174]

    padding = package[174:184]
    
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
    package_header = package[:8]
    checksum = package[88:96]

    if package[8:10] == '31':
        s1 = package[10:14]
        unix = package[14:22]

        s2 = package[22:26]
        rest = package[26:88]
    elif package[8:10] == '30':
        s1 = package[10:16]
        unix = package[16:24]

        rest = package[24:88]
    else:
        raise "Wong"

def decode_14(package: str):
    header = package[:6]
    s0 = package[6:16]
    unix = package[16:24]
    s1 = package[24:40]
    checksum = package[40:48]

def decode_44(package: str):
    header = package[:10]
    assert header == "aa44000f32", "Different header"

    s0 = package[10:12] # Some kind of counter

    assert int(package[12:14], 16) == 2
    assert int(package[14:16], 16) == 0

    s1 = package[16:22]

    assert int(package[22:24], 16) == 102
    crc = package[24:26] # This seems to increment by 8 after every 3 entries

    s2 = package[26:28]

    assert int(package[28:30], 16) == 52
    assert int(package[30:32], 16) == 0
    assert int(package[32:34], 16) == 1
    

    data = package[34:134] # This data is most of packet idk what it is, it seems to octagonally repeat shifted, example:
    # 32 30 38 31 3a (20 42 4c 45 3a 20 48 45 4c) 4c 4f 3a 20 46 47 20 53 4f 43 20 28 74 65 6e 74 68 73 29 3a 20 32 34 39 0a 20 20 39 2c 20 31 33 35 39 31 32
    # 30 38 33 3a (20 42 4c 45 3a 20 48 45 4c) 4c 4f 3a 20 4e 6f 72 64 69 63 20 56 65 72 3a 20 31 37 2e 32 2e 32 2e 30 0a 20 20 39 2c 20 31 33 35 39 31 32 31
    # 30 35 3a (20 42 4c 45 3a 20 48 45 4c) 4c 4f 3a 20 52 65 70 6f 72 74 69 6e 67 20 63 68 61 72 67 65 20 73 74 61 74 65 20 61 73 3a 20 30 0a 20 20 39 2c 20
    # 31 33 35 39 31 32 31 30 36 3a (20 42 4c 45 3a 20 48 45 4c) 4c 4f 3a 20 53 65 6e 64 20 68 65 6c 6c 6f 20 70 61 63 6b 65 74 0a 20 20 39 2c 20 31 33 35 39
    # 31 32 31 30 36 3a (20 42 4c 45 3a 20 48 45 4c) 4c 4f 3a 20 47
    # but this might just be an accident

    assert int(package[134:136], 16) == 0
    checksum = package[136:144]

def decode_0c(package: str):
    header = package[:10]
    assert header == "aa0c00fc24", "Invalid header"

    crc = package[10:12] # Seems to increment by 3

    data = package[12:20]

    padding = package[20:24]
    assert int(padding, 16) == 0

    checksum = package[24:32]

def decode_18(package: str):
    header = package[:8]
    assert header == "aa1800ff", "Invalid header"

    if package[8:10] == '28':
        unix = package[12:20]
        s0 = package[20:22]
        crc = package[22:24]
        s1 = package[24:48]
    elif package[8:10] == '30':
        s0 = package[8:16]
        unix = package[16:24]
        s1 = package[24:48]
    else:
        raise "Unsupported"

    checksum = package[48:56]