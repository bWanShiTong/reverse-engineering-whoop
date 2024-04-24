from misc import *
import numpy as np
from os import listdir
from json import dumps
from time import time

files = listdir('./data')
FILE = None
FILE = "captured-packages-write.txt"

def find_unix(packet: str):
    size = 8

    for i in range(0, len(packet), 2):
        data = packet[i:i+size]
        if len(data) != size:
            return

        unix = little_endian(data)
        if earliest_unix < unix and unix < latest_unix:
            return i

def find_value(packet: str):
    SIZE = 4
    for i in range(0, len(packet), 2):
        if len(packet[i:i+SIZE]) != SIZE:
            continue
        
        print(little_endian(packet[i:i+SIZE]))

findings = {}
for file in files:
    if FILE:
        if file == FILE:continue

    data = open(f'data/{file}', 'r').read().split('\n')

    for package in data:
        header = package[2:4]
        if not header:
            continue

        if position := find_unix(package):
            if exists := findings.get(header):
                exists.append(position)
            else:
                findings[header] = [position]

for header, positions in findings.items():
    print(header, len(positions), {i: positions.count(i) for i in positions})