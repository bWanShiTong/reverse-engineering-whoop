data = open('data/61080003-8d6d-82b8-614a-1c8cb0f8dcc6.txt', 'r')

s = {}

for line in data.readlines():
    line = line.strip()
    if s.get(line[2:4]):
        s[line[2:4]].append(len(line))
    else:
        s[line[2:4]] = [len(line)]

for char, lengths in s.items():
    assert all([lengths[0] == i for i in lengths])
    bytes_length = int(char, 16)
    length_in_bytes = lengths[0] / 2 - 4 # Take length of string divide by 2 since 2 hex chars are 1 byte, and remove 4 since that is size of header
    assert bytes_length == length_in_bytes