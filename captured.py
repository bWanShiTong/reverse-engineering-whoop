from pandas import read_csv
from json import dumps

from misc import *

df = read_csv('captured.txt', sep=';')

missing = {}
for row in df.iloc:
    data = row.data
    func = globals().get(f"decode_{data[2:4]}")
    if func is None:
        missing[data[2:4]] = missing.get(data[2:4]) + 1 if missing.get(data[2:4]) else 1
    else:
        func(data)

print(dumps(missing, indent=4))