files = [
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.05.txt',
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.22.txt',
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.18.38.txt',
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.18.49.txt',
]

for file in files:
    print(file)
    data = open(file, 'r').read().split('\n')

    for buffer in data:
        header = buffer[:12]

        timestamp = ' '.join([buffer[12:20][i:i+2] for i in range(0, 8, 2)][::-1]) # Little endian timestamp

        s = buffer[26:44]
        s = [s[i:i+2] for i in range(0, len(s), 2) if s[i:i+2]]
        s = ' '.join(s)
        
        print(f'{header}\t{timestamp}\t{buffer[20:24]}\t{buffer[24:26]}  {s}  {buffer[44:48]}\t{buffer[48:]}')