from misc import *
import numpy as np
from os import listdir
from json import dumps

files = listdir('./data')
FILE = None
# FILE = "captured-packages-write.txt"


packages = {}

for file in files:
    if FILE:
        if not file == FILE:continue

    if file == "captured-packages-write.txt":continue

    data = open(f'data/{file}', 'r').read().split('\n')

    for package in data:
        header = package[2:4]
        if not header:
            continue

        if header_packages := packages.get(header):
            header_packages.append(package)
        else:
            packages[header] = [package]


packages = {i: list(dict.fromkeys(j)) for i,j in packages.items()}
missing = {}

for package_type in packages:
    packages_ = packages[package_type]
    function = globals().get(f"decode_{package_type}")
    if function is None:
        missing[package_type] = len(packages_)
        continue

    for package in packages_:
        function(package)

# packages = {i: len(j) for i,j in packages.items()}
# print(dumps(packages, indent=4))

if missing:
    print(dumps(missing, indent=4))