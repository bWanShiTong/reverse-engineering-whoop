from misc import *
import numpy as np

files = [
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6.txt',
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-reloading-20.50.txt',
    '61080005-8d6d-82b8-614a-1c8cb0f8dcc6-reloading-22.25-after-5mins.txt'
]


packages = {}

for file in files:
    data = open(file, 'r').read().split('\n')

    for package in data:
        header = package[2:4]
        if header_packages := packages.get(header):
            header_packages.append(package)
        else:
            packages[header] = [package]


packages = {i: list(dict.fromkeys(j)) for i,j in packages.items()}

for package in packages['2c']:
    print(package)

print(packages.keys())