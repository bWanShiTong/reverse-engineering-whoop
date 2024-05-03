from misc import *
from json import dumps

packages = load_data()
missing = {}

for package_type in packages:
    packages_ = packages[package_type]
    function = globals().get(f"decode_{package_type}")
    if function is None:
        missing[package_type] = len(packages_)
        continue

    for package in packages_:
        function(package)

packages = {i: len(j) for i,j in packages.items()}
# print(dumps(packages, indent=4))

# if missing:
#     print(dumps(missing, indent=4))