from os import listdir

def check_lengths(file: str):
    data = open(f'data/{file}', 'r')

    s = {}

    for line in data.readlines():
        line = line.strip()
        bytes_length = int(line[2:4], 16)
        if bytes_length == 0:
            continue

        length_in_bytes = len(line[4:]) / 2 - 2 # Take length of string divide by 2 since 2 hex chars are 1 byte, and remove 2 since that is size of header in bytes
        assert bytes_length == length_in_bytes, f"Expected length: {bytes_length}, actual: {length_in_bytes}, packet: {line}"

for file in listdir('./data'):
    if file == "captured-packages-write.txt":continue
    check_lengths(file)