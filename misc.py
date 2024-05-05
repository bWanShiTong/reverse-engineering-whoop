from datetime import datetime
from dataclasses import dataclass
from time import time
from os import listdir
from pandas import read_csv

latest_unix = round(time()) + 10640000
earliest_unix = 1711234800

def hex_to_ascii(data: str):
    return bytearray.fromhex(data).decode(encoding='ascii')

def rr_readings(buffer: str):
    buffer = bytearray.fromhex(buffer)
    n = buffer[0]

    rr = []
    if n > 0:
        buffer = buffer[1:]
        for i in range(0, n):
            buf = buffer[i*2:i*2+2]
            rr.append(int.from_bytes(buf, 'little'))

    return rr

def check_constants(constants_):
    def decorator(func):
        def wrapper(buf, **kwargs):
            for i, j in constants_.items():
                i = int(i)
                constants(buf[i:i+2], j)

            return func(buf)

        return wrapper

    return decorator

def hex_to_array(buf: str):
    return [int(buf[i:i+2], 16) for i in range(0, len(buf), 2)]

def constants(buf: str, const: str):
    assert buf == const, f"Expected: {const}, but is {buf}"

def load_data(FILE: str = None):
    packages = {}

    def append(data: str):
        header = data[2:4]
        if not header or header == "00":
            return

        if header_packages := packages.get(header):
            header_packages.append(data)
        else:
            packages[header] = [data]

    if FILE == "captured.txt" or not FILE:
        df = read_csv('captured.txt', sep=';')
        for row in df.iloc:
            data = row.data
            append(data)

    for file in listdir('./data'):
        if FILE:
            if not file == FILE:continue

        if file == "captured-packages-write.txt" and file != FILE:continue

        data = open(f'data/{file}', 'r').read().split('\n')

        for package in data:
            append(package)

    return {i: list(dict.fromkeys(j)) for i,j in packages.items()}

def padding(buf):
    assert int(buf, 16) == 0, f"Non zero padding: {buf}"

def little_endian(buffer: str) -> int:
    return int.from_bytes(bytearray.fromhex(buffer), 'little')

def big_endian(buffer: str) -> int:
    return int.from_bytes(bytearray.fromhex(buffer), 'big')

def check_unix(data: str) -> int:
    unix = little_endian(data)
    assert earliest_unix < unix and unix < latest_unix, f"Not a unix: {unix}, {data}"
    return unix

def pretty_print(buffer: str, as_int: bool=False):
    buffer = [str(int(buffer[i:i+2], 16)).ljust(4) if as_int else buffer[i:i+2] for i in range(0, len(buffer), 2)]
    print(' '.join(buffer))

def print_raw(buffer: str):
    size = len(buffer) * 4
    print(f"{int(buffer, 16):0>{size}b}")

# This packages is sent and received on WHOOP_CHAR_MEMFAULT
def decode_02(package: str):
    header = package[:4]
    assert header == "0802", "Invalid header"

def decode_24(package: str):
    header = package[:10]
    assert header == "aa2400fa30", "Invalid header"

    s0 = package[10:16] # seems to be around 700-1000 but not enough samples

    unix = check_unix(package[16:24])
    s1 = package[24:28]

    assert package[28:30] == "14"
    assert package[30:32] == "00"
    assert package[32:34] == "02"

    s2 = little_endian(package[34:42])
    assert 200 < s2 and s2 <= 1000, f"Invalid range: {s2}"

    s3 = little_endian(package[42:50])
    assert 3700 < s3 and s3 < 4400, f"Invalid range: {s3}"
    # s2 and s3 seem to be correlated, when one is on lower range second one is too
    
    assert package[50:54] == "0000" or package[50:54] == "0101", f"Invalid: {package[50:54]}" # Seem to be some kind of flags

    s4 = package[54:62] # Not sure what any of these are

    # if byte 62:64 is > 0 then byte 64:66 is 0
    # if byte 62:64 is 0 then byte 64:66 is 1
    flags = package[62:66] # Some kind of flags

    padding(package[66:72])

    checksum = package[72:80]

# Main package
def decode_5c(package: str, verbose: bool = False):
    header = package[:12]
    assert header == "aa5c00f02f0c", f"Invalid header: {header}"

    s0 = package[12:14]
    unix_s = package[14:20]
    padding(package[20:22])
    unix_e = check_unix(package[22:30])
    if verbose:
        print(datetime.utcfromtimestamp(unix_e), end='\t')

    crc_1 = package[30:32] # Seems to increment by 8
    crc_2 = package[32:34] # Seems to decrement by 5

    s0 = package[34:38] # These seem to be flags, 1000 0{0,1}00
    s2 = package[38:40]
    
    s3 = package[40:42]
    # assert s3 == "01" or s3 == "00"

    s00 = little_endian(package[38:42])
    # assert 200 <= s00 and s00 <= 550, f"Invalid range: {s00}"

    heart_rate = int(package[42:44], 16) # ?
    if verbose:
        print(f"HR: {heart_rate}({package[42:44]})", end='\t')

    rr = rr_readings(package[44:62])

    flags0 = package[62:66]
    data0 = package[66:104] # IDK what this is, but it is not gyroscope or accelerometer, since its values don't change with rotation of device or moving of device
    if verbose:
        pretty_print(data0, True)
    
    padding(package[104:106])

    flags1 = package[106:110]
    data1 = package[110:170]


    padding(package[170:172])

    flags = package[172:174] # ?

    padding(package[174:182])

    s4 = package[182:184]
    checksum = package[184:]

# When this packet is sent data is other values are received
def decode_08(package: str):
    header = package[:10]
    assert header == "aa0800a823", "Invalid header"

    pc = int(package[10:12], 16) # Increments constantly but next value doesn't increment after overflow
    s0 = package[12:16] # IDC, first byte seems to change, while next byte is either 1 or 0
    checksum = package[16:24]

def decode_1c(package: str):
    header = package[:8]
    assert header == "aa1c00ab", "Invalid header"

    package_type = package[8:10]
    match package_type:
        case '30':
            s0 = little_endian(package[10:16]) # This seems to be incrementing maybe a package count
            unix = check_unix(package[16:24])

            s1 = package[24:48]
            
            d0 = package[48:56]
        case '31':
            crc = package[10:12] # Increments by 3
            s0 = package[12:14] # either 0 or 2

            unix = check_unix(package[14:22]) # ?

            temperature = little_endian(package[22:34]) / 100000 # ?
            
            if package[34:50] != "ffffffffffffffff":
                crc = package[34:36] # Increments by 5
                s0 = package[36:44]
                padding(package[44:56])
        case '24':
            s0 = package[10:24]
            padding(package[24:56])
        case package_type:
            print(package_type)
            raise "Wong"

    checksum = package[56:64]
    

def decode_10(package: str):
    header = package[:8]
    assert header == "aa100057", "Invalid header"

    package_type = package[8:10]
    
    match package_type:
        case "31":
            data = little_endian(package[10:14]) # always around 1000
            unix = check_unix(package[14:22]) # not sure 100%
            s0 = package[22:26]

            padding(package[26:32])
        case "30":
            data = package[10:16]
            unix = check_unix(package[16:24]) # not sure 100%
            s0 = package[24:28]

            padding(package[28:32])
        case "23":
            pc = little_endian(package[10:12]) # Increments by 1 but after overflow it doesn't increase next value
            s0 = little_endian(package[12:14])
            # As mentioned above byte [10:12] increments by 1, but after overflow it goes to 0, without byte [12:14] incrementing
            # But pc value sometimes resets without overflowing and byte [12:14] changes from 23 to 66
            match s0:
                case 23:
                    s1 = package[14:16] # Either 0 or 1
                    sometime = little_endian(package[16:20]) # Byte [16:18] seems to increment by 1 every time and after overflow byte [18:20] increments
                    # These seems to be some kind of time since something not sure what
                    s2 = package[20:22] # Either 0 or 1
                    if 65535 == sometime:
                        assert package[16:32] == "ffffffffffffffff"
                    else:
                        s3 = package[22:24] # Either 0 or 1
                        constants(package[22:26], "0002")
                        padding(package[26:32])

                case 66:
                    next_day_alarm = datetime.utcfromtimestamp(little_endian(package[16:24]))
                    padding(package[24:32])
                case 10:
                    s0 = package[14:26] # Seems like unix but isn't
                    padding(package[26:32])
                case x:
                    print(x)
                    raise "Wong"
        case "24":
            s0 = package[10:18]
            has_unix = little_endian(package[18:20]) == 1
            if has_unix:
                next_day_alarm = little_endian(package[20:28])
                padding(package[28:32])
            else:
                padding(package[20:32])
        case x:
            print(x)
            raise

    header = package[32:40]

def decode_2c(package: str):
    package_header = package[:8]

    if package[8:10] == '31':
        s1 = package[10:14]
        unix = check_unix(package[14:22])

        s2 = package[22:26]
        rest = package[26:88]
    elif package[8:10] == '30':
        s1 = package[10:16]
        unix = check_unix(package[16:24])

        rest = package[24:88]
    elif package[8:10] == '24':
        # pretty_print(package[10:60])
        padding(package[62:88])
    else:
        print(package[8:10])
        raise "Wong"

    checksum = package[88:96]

def decode_14(package: str):
    header = package[:6]
    s0 = package[6:16]
    unix = check_unix(package[16:24])
    s1 = package[24:40]
    checksum = package[40:48]

def decode_44(package: str):
    header = package[:8]
    assert header == "aa44000f", f"Different header: {header}"

    s0 = package[8:12] # Some kind of counter

    # assert int(package[12:14], 16) == 2
    assert int(package[14:16], 16) == 0

    s1 = package[16:22]

    assert int(package[22:24], 16) == 102
    crc = package[24:26] # This seems to increment by 8 after every 3 entries

    s2 = package[26:28]

    assert int(package[28:30], 16) == 52
    assert int(package[30:32], 16) == 0
    assert int(package[32:34], 16) == 1
    
    data = bytearray.fromhex(package[34:134]).decode(encoding='ascii')
    # This is some kind of log ex:
    #   BLE: History burst success. Trim: 0x00000000:0000
    #   BLE: Enabled Entry.
    #   BLE: Command Send Historical D
    print(data)

    assert int(package[134:136], 16) == 0
    checksum = package[136:144]

def decode_0c(package: str):
    header = package[:8]
    assert header == "aa0c00fc", "Invalid header"

    data = package[8:24]
    
    checksum = package[24:32]

def decode_18(package: str):
    header = package[:8]
    assert header == "aa1800ff", "Invalid header"

    if package[8:10] == '28':
        unix = check_unix(package[12:20])
        crc = package[20:24]
        heart_rate = little_endian(package[24:26])
        rr = rr_readings(package[26:44])
        flags = package[44:48]
    elif package[8:10] == '30':
        s0 = package[8:16]
        unix = check_unix(package[16:24])
        s1 = package[24:48]
    else:
        raise "Unsupported"

    checksum = package[48:56]


def decode_48(package: str):
    # 15, 14, 12, 11:37, NO alrams
    header = package[:10]
    assert header == "aa4800f323", "Invalid header"

    packet_count = package[10:12] # Not sure but seems to increment with every sent package
    assert package[12:14] == "78"
    assert package[14:16] == "01"

def decode_8c(packet: str):
    # print(packet[10:])
    header = packet[:10]
    assert header == "aa8c004a24", "Invalid header"
    data = packet[10:24] 
    # bytes [10:14] seems to be around 9000
    # byte [14:16] is mostly 00
    # byte [16:18] is 01
    # byte [18:20] is 04
    # byte [20:22] seems to be some value
    # byte [22:24] is 01, 02, 03

    padding(packet[24:30])
    unix = check_unix(packet[30:38]) # ? not sure
    s0 = packet[38:42]

    data = packet[42:246]
    const = "000034433131313338373000613732343530623337353631343432623266366332313464653962626130396336313164386437643436633636643635333235663062060000000200000010000000290000000f00000003000000000000000800000100000000"
    assert data == const, data
    s1 = packet[246:248]

    const = "110000000200000002"
    assert packet[248:266] == const, packet[248:266]

    padding(packet[266:280])
    checksum = packet[280:288]

def decode_4c(packet: str):
    header = packet[:10]
    assert header == "aa4c00a724"
    
    # byte at 10:12 seems to be incrementing while byte at 12:14 doesn't increment after 10:12 overflows
    # byte at 14:16 also increments but next byte doesn't change and is always 1
    s0 = packet[10:16]
    
    assert int(packet[16:18], 16) == 1, "Not a one"
    assert int(packet[18:20], 16) == 1, "Not a one"

    data = packet[20:56]

    padding = packet[56:84]
    assert int(padding, 16) == 0, "Non zero padding"
    
    tt = packet[84:86]
    assert tt == "32"

    padding = packet[86:152]
    assert int(padding, 16) == 0, "Non zero padding"
    checksum = packet[152:160]