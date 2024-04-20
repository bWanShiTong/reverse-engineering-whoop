from pandas import read_csv
from json import dumps

from misc import *

df = read_csv('captured.txt', sep=';')

missing = {}
packages = {}
for row in df.iloc:
    data = row.data
    func = globals().get(f"decode_{data[2:4]}")

    if packages.get(row.characteristic) is None:
        packages[row.characteristic] = {}

    packages[row.characteristic][data[2:4]] = packages[row.characteristic].get(data[2:4]) + 1 if packages[row.characteristic].get(data[2:4]) else 1
    if func is None:
        missing[data[2:4]] = missing.get(data[2:4]) + 1 if missing.get(data[2:4]) else 1
    else:
        func(data)


print(dumps(packages, indent=4))

if missing:
    print(dumps(missing, indent=4))