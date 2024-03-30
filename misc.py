def little_endian_unix(buffer: str) -> int:
    buffer = [buffer[i:i+2] for i in range(0, 8 , 2)][::-1]
    return int(''.join(buffer), 16)


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

    s1 = package[34:38]
    padding = package[38:56]
    assert int(padding, 16) == 0, "Non zero padding"

    checksum = package[56:]
    print(len(checksum) / 2)