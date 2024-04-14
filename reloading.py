from misc import *
import numpy as np
from os import listdir

files = listdir('./data')

packages = {}

for file in files:
    if not file == "captured-packages-read.txt":continue
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

for package_type in packages:
    packages_ = packages[package_type]
    function = globals().get(f"decode_{package_type}")
    if function is None:
        print(f"{package_type} not found: {len(packages_)}")
        continue

    for package in packages_:
        function(package)