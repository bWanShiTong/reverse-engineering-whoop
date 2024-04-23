# Reverse Engineering Whoop 4.0

This is my attempt to reverse engineer Whoop 4.0,


## Data fetching

Packets can be obtained with app found in [record-app](./record-app/), app finds device whose name starts with WHOOP and subscribes to all characteristics to get data, which can be transferred with [server.py](./server.py).

Or using [extract-logs.sh](./extract-logs.sh) and [parse_pcap.py](./parse_pcap.py) to get bluetooth logs from android using adb.

## Data decoding

Notes of decoding can be found in [DECODING](./DECODING.md) and functions that decode in [misc.py](./misc.py). 