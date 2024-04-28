from misc import *
from json import dumps

data = load_data()

package = '5c'

def find_constants(package: str):
    constants = {}
    for i in range(1, len(data[package])):
        prev = data[package][i-1]
        cur = data[package][i]

        for j in range(0, len(prev), 2):
            if int(prev[j:j+2] ,16)- int(cur[j:j+2],16) == 0 and (constants.get(j) == 0 or constants.get(j) is None):
                constants[j] = True
            else:
                constants[j] = False

    constants = [i for i,j in constants.items() if j]
    print(dumps(constants, indent=4))

find_constants(package)