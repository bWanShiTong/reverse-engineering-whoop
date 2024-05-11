# Reverse Engineering Whoop 4.0

This is my attempt to reverse engineer Whoop 4.0,


## Data fetching

Packets can be obtained with app found in [record-app](./record-app/), app finds device whose name starts with WHOOP and subscribes to all characteristics to get data, which can be transferred with [server.py](./server.py).

Or using [extract-logs.sh](./extract-logs.sh) and [parse_pcap.py](./parse_pcap.py) to get bluetooth logs from android using adb.

## Data decoding

Notes of decoding can be found in [DECODING](./DECODING.md) and functions that decode in [misc.py](./misc.py). 

## Current Progress

Some of write commands have be identified but I can identify algo used to calculate checksum, so I can't test these commands.
Currently it seems that sending `aa0800a8230e16001147c585` to `61080002-8d6d-82b8-614a-1c8cb0f8dcc6` returns last few minutes of values.

Repo attempting to emulate whoop can be found [here](https://github.com/bWanShiTong/whoop-simulator)