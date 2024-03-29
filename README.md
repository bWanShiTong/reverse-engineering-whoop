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

#### 61080002-8d6d-82b8-614a-1c8cb0f8dcc6

Writeable and Writeable without response, my opinion is that this is for setting alarm.

#### 61080003-8d6d-82b8-614a-1c8cb0f8dcc6

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

First 4 hex characters should be header, hex character should be 4 bits

First character should be PDU Type (4 bits), second should be RFU, ChSel, TxAdd and RxAdd (each is 1 bit), and remaining two should be Length (8 bits) in bytes.

`00` is some separator or padding, next 4 characters (16 bits) seem to be same on packages of same length, with last 2 characters always being 24.

After that rest should be data, there are few values it should transmit one is heart rate, temperature and Sp02, heart rate is commonly represented as `uint8` which has range of 0-255, temperature could be 0-100 for celsius or 32-212 for Fahrenheit, meaning that both of those should be represented by `uint8` and Sp02 should be between 0-100 so it can also be represented by `uint8`.

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

#### 61080004-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

#### 61080005-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

Messages for this characteristic are [here](./61080005-8d6d-82b8-614a-1c8cb0f8dcc6.txt)



#### 61080007-8d6d-82b8-614a-1c8cb0f8dcc6

-||-