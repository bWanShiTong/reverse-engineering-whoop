# Reverse Engineering Whoop 4.0

## Services

Whoop 4.0 has following bluetooth services

### Device information: 0000180a-0000-1000-8000-00805f9b34fb

Has one characteristic `Manufacturer Name String` which returns `WHOOP Inc.`

### Generic Access: 00001800-0000-1000-8000-00805f9b34fb

Has 4 characteristics: `DEVICE NAME`, `APPEARANCE`, `PERIPHERAL PREFERRED CONNECTION PARAMETERS` and `CENTRAL ADDRESS RESOLUTION`.

### Generic Attribute: 00001801-0000-1000-8000-00805f9b34fb

Has 1 characteristic: `SERVICE CHANGED`

### Bond Management: 0000181e-0000-1000-8000-00805f9b34fb

Has 2 characteristics: `BOND MANAGEMENT FEATURE` and `BOND MANAGEMENT CONTROL POINT`

### Heart Rate: 0000180d-0000-1000-8000-00805f9b34fb

Has simple characteristic which is notifiable and broadcasts heart rate

### Battery Service: 0000180f-0000-1000-8000-00805f9b34fb

Has simple characteristic to read battery level can also be notifiable

### Special Sauce: 61080001-8d6d-82b8-614a-1c8cb0f8dcc6

This is custom service where magic happens it has following characteristic:

#### WHOOP_CHAR_CMD_TO_STRAP 61080002-8d6d-82b8-614a-1c8cb0f8dcc6

Writeable and Writeable without response, my opinion is that this is for setting alarm.

#### WHOOP_CHAR_CMD_FROM_STRAP 61080003-8d6d-82b8-614a-1c8cb0f8dcc6

Messages for this characteristic are [here](./61080003-8d6d-82b8-614a-1c8cb0f8dcc6.txt) they are in hex.

These are few of those messages of different lengths:

```
aa0c00fc24b4170001000000308d4b6a
aa0c00fc24b7170001000000ad97a35b
aa0c00fc24ba1700010000006df6743a
aa2c0052243b765a0101000167656e6572616c5f61625f746573740000000000000000000000000000000000ffcdfdd0
aa2c0052243c765b0101010173696770726f635f31305f7365635f647000000000000000000000000000000020449296
aa2c0052243d765c0101020173696770726f635f706461660000000000000000000000000000000000000000e532217f
aa2c0052243e765d01010301656e61626c655f7231395f7061636b65747300000000000000000000000000007e5d5f45
aa4c00a7243f785e010167656e6572616c5f61625f746573740000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000000003f37ae05
aa4c00a72440785f010173696770726f635f31305f7365635f647000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000000000a2c6ef96
aa4c00a724417860010173696770726f635f70646166000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000000000cb9b2f0b
```

Broken down:

First 4 hex characters should be header, hex character is 4 bits

First character should be PDU Type (4 bits), second should be RFU, ChSel, TxAdd and RxAdd (each is 1 bit), and remaining two are Length (8 bits) in bytes.

`00` is some separator or padding, next 4 characters (16 bits) seem to be same on packages of same length, with last 2 characters always being 24.

After that rest should be data, there are few values it should transmit one is heart rate, temperature and Sp02, heart rate is commonly represented as `uint8` which has range of 0-255, temperature could be 0-100 for celsius or 32-212 for Fahrenheit, meaning that both of those should be represented by `uint8` and Sp02 should be between 0-100 so it can also be represented by `uint8`.

If we look at data from [WHOOP_CHAR_DATA_FROM_STRAP](#whoop_char_data_from_strap-61080005-8d6d-82b8-614a-1c8cb0f8dcc6) we can see that header is same first 8 bits being aa, second two being Length, then separator/padding of `00`

```
Header      Payload
aa0c        00  fc24    a2 16 54 02 0b 00 00 65 de 6a 76
aa0c        00  fc24    b7 17 00 01 00 00 00 ad 97 a3 5b
aa0c        00  fc24    ba 17 00 01 00 00 00 6d f6 74 3a
aa2c        00  5224    3b765a0101000167656e6572616c5f61625f746573740000000000000000000000000000000000ffcdfdd0
aa2c        00  5224    3c765b0101010173696770726f635f31305f7365635f647000000000000000000000000000000020449296
aa2c        00  5224    3e765d01010301656e61626c655f7231395f7061636b65747300000000000000000000000000007e5d5f45
aa4c        00  a724    3f785e010167656e6572616c5f61625f746573740000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000000003f37ae05
aa4c        00  a724    40785f010173696770726f635f31305f7365635f647000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000000000a2c6ef96
aa4c        00  a724    417860010173696770726f635f70646166000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000000000cb9b2f0b
```

Notifiable characteristic

#### WHOOP_CHAR_EVENTS_FROM_STRAP 61080004-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

#### WHOOP_CHAR_DATA_FROM_STRAP 61080005-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

Messages for this characteristic are [here](./61080005-8d6d-82b8-614a-1c8cb0f8dcc6.txt)

Messages when health monitor is opened are [here](./61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.05.txt) this was recorded on 29.3.2024 around 17:05, with heart rate being 75 at start going to 101 and back to 75, each log is about a second apart. and there is another log [here](./61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.22.txt) recorded at 17:22, with heart rate being around 78.

Here is a part of logs:

Header seems to be `aa1800ff2802`, next 32 bits represent unix timestamp.
I dont know what next 16 bits represent, but first byte seems to increment in decimal by 0, 8 or 16, and next byte seems to decrement by 5, until overflow.

Next byte is heart rate.

I don't know what next 68 bits are but they seem to either be 0 or something, I am not sure what that something should be,

- First byte seems to represent how many pairs of bytes are there `01` being two bytes, `02` being four bytes and `03` being 6 bytes, this could maybe go up two `04` or `05` depending on whether 16 bits in front of `0101` are part of this.
- Next byte as int is in range of 10-248
- Next byte is number in range of 1-7
- Next byte if present is in range of 17-244
- Next byte if present is either `02` or `03`, this might be due to lack of data
- Only 1 entry with this byte
- -||-

Guesses on what this is,

- Sensor data, but not sure in what format, initial idea was that first number is measurement and second being sensor index, sort of `01` for temperature, `02` for Sp02 and so on, but numbers can repeat, and max is 7
- Checksum?
- Blood oxygen only with first being reading of sensor and second being integrity, [here is why](https://www.reddit.com/r/whoop/comments/s0ojs0/any_way_to_see_blood_oxygen_spo2_levels_over_time/)

Next `0101` seems to be another separator with last 4 bytes being checksum

```
Header          Unix                    HR  S
aa1800ff2802    0f e6 06 66     6045    45  00 00 00 00 00 00 00 0000  0101     100092bd
aa1800ff2802    10 e6 06 66     7040    45  00 00 00 00 00 00 00 0000  0101     1f77d31e
aa1800ff2802    11 e6 06 66     803b    45  00 00 00 00 00 00 00 0000  0101     7e5ea0c5
aa1800ff2802    12 e6 06 66     8836    45  00 00 00 00 00 00 00 0000  0101     54fd535b
aa1800ff2802    13 e6 06 66     9831    45  00 00 00 00 00 00 00 0000  0101     8171c0af
aa1800ff2802    14 e6 06 66     982c    45  00 00 00 00 00 00 00 0000  0101     41bdc5bd
aa1800ff2802    15 e6 06 66     b027    45  00 00 00 00 00 00 00 0000  0101     edd2634b
...
aa1800ff2802    95 e6 06 66     0015    4d  00 00 00 00 00 00 00 0000  0101     a0b184ac
aa1800ff2802    96 e6 06 66     0010    4c  02 66 06 11 02 00 00 0000  0101     5e078910
aa1800ff2802    97 e6 06 66     180b    4c  01 30 04 00 00 00 00 0000  0101     88126edd
aa1800ff2802    98 e6 06 66     2006    4c  01 bd 02 00 00 00 00 0000  0101     27775394
aa1800ff2802    99 e6 06 66     3001    4c  02 6c 03 d6 02 00 00 0000  0101     75036709
aa1800ff2802    99 e6 06 66     387c    4c  01 83 03 00 00 00 00 0000  0101     f65f00cf
aa1800ff2802    9a e6 06 66     4077    4c  00 00 00 00 00 00 00 0000  0101     43c148ee
...
aa1800ff2802    b8 fc 06 66     b809    67  01 55 02 00 00 00 00 0000  0101     cda31650
aa1800ff2802    b9 fc 06 66     b804    67  01 4e 02 00 00 00 00 0000  0101     4d0f2627
aa1800ff2802    b9 fc 06 66     d07f    67  03 66 02 12 02 46 02 0000  0101     fe3ab9cb
aa1800ff2802    ba fc 06 66     d87a    68  01 6b 02 00 00 00 00 0000  0101     d77a8fda
aa1800ff2802    bb fc 06 66     e875    68  01 39 02 00 00 00 00 0000  0101     c20b9a04
```

While switch between whoop app and random app [logs](./61080005-8d6d-82b8-614a-1c8cb0f8dcc6-reloading-20.50.txt):

It seems that ending packages with start of `aa10` are last ones in load

Packages with header `aa5c`

These packages have similar design as ones above

```
aa5c00f02f0c050058070074310766704c80542c0147015c0300000000000000008f05ff002ec43bcd8c92bdaeb7be3ef6647b3f0000c446cd8c92bdaeb7be3ef6647b3f390253025903520241016005010c020c0000000000000001f32f9943
aa5c00f02f0c050058070074310766704c80542c0147015c0300000000000000008f05ff002ec43bcd8c92bdaeb7be3ef6647b3f0000c446cd8c92bdaeb7be3ef6647b3f390253025903520241016005010c020c0000000000000001f32f9943
aa5c00f02f0c050d58070081310766080c80542c0146015f030000000000000000d900ff804d823cd78398bd8533b83ecd7c7c3f0000e046d78398bd8533b83ecd7c7c3f390253025c03540241016005010c020c0000000000000001f5aa1154
aa5c00f02f0c050d58070081310766080c80542c0146015f030000000000000000d900ff804d823cd78398bd8533b83ecd7c7c3f0000e046d78398bd8533b83ecd7c7c3f390253025c03540241016005010c020c0000000000000001f5aa1154
```

First 7 bytes being header. Next 3 bytes being seconds or some kind of time (NOT UNIX), then 1 byte separator, next 4 bytes being unix, then next 2 bytes being same as packet about where first is incrementing and second decrementing.

Next byte is either `80` or `84` in hex, next byte is always `54`, next 2 bytes sometimes change but don't know to what.

Next byte seems to be heart rate.

Next 7 bytes could be some kind of integer, not sure what.

Next 2 bytes are padding.

Next 21 bytes seem to be some data:

* First 4 bytes seem to be something
    - First byte is either 0 or 128
* Next bytes seems to be big integer, mostly `ff`
* Next 3 bytes IDK
* Next byte seems to be heart rate
* Next 3 bytes IDK
* Next byte seems to be only around 60 or around 190
* Next 3 bytes IDK
* Next bytes is around 60 with few outliers around 190
* Next 3 bytes IDK
* Next bytes is around 63 with few outliers around 190

Notes:
* These pairs of 4 bytes where first 3 bytes are "random" and next byte being seeming to be heart rate, could be some type of heart rate occurrences.

Next 32 bytes seem to be similar to data above:

* First byte seems to be mostly zero.
* Next 5 bytes IDK
* Next byte seems to be either around 60 or 190
* Next 3 bytes IDK
* Next bytes is around 60 with few outliers around 190
* Next 3 bytes IDK
* Next bytes is around 63 with few outliers around 190
* Next byte is either in decimal 11, 26, 30 or 57, this might be due to lack of data
* Next byte is `02`
* Next bytes changes with byte before where 11=92, 26=107, 30=111, 57=83
* Next byte is `02`
* Next bytes middle value changes with two bytes before, where for first bytes value being 11, this was around 140, first bytes being 26, this was around 10, etc.
* Next byte is either `03` or `04`
* Next byte seems to be somewhat connected with previous byte
* Next byte is `02`
* Next byte is sort of changing
* Next byte is `01`
* Next byte has few values, decimal: 96, 80, 160
* Next byte is either `03`, `04`, `05` or `06`
* Next 4 bytes seem to be `010c020c`
* Next byte seems to be small < 16 number

Next 7 bytes are padding 

Remaining bytes seem to be checksum

Packages with header `aa1c`

First 7 bytes are header, next 8 bytes seem to be unix, 

Next 3 bytes are some data

Next 6 bytes seem to be padding

Next 2 bytes are some data

Next 9 bytes seem to be padding

And last 4 bytes seem to be checksum

What these two data packages represent i dont know, it seems semi random, need to check with context of packets before.

#### WHOOP_CHAR_MEMFAULT 61080007-8d6d-82b8-614a-1c8cb0f8dcc6

-||-
