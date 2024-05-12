## Services

Whoop has general few services including one for heart rate and battery that allows for devices to be used, following service is custom.

### Special Sauce: 61080001-8d6d-82b8-614a-1c8cb0f8dcc6

This is custom service where magic happens it has following characteristic:

#### WHOOP_CHAR_CMD_TO_STRAP 61080002-8d6d-82b8-614a-1c8cb0f8dcc6

Writeable and Writeable without response, my opinion is that this is for setting alarm.

#### WHOOP_CHAR_CMD_FROM_STRAP 61080003-8d6d-82b8-614a-1c8cb0f8dcc6

Messages for this characteristic are [here](./data/61080003-8d6d-82b8-614a-1c8cb0f8dcc6.txt) they are in hex.

Notifiable characteristic

#### WHOOP_CHAR_EVENTS_FROM_STRAP 61080004-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

#### WHOOP_CHAR_DATA_FROM_STRAP 61080005-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

Messages for this characteristic are [here](./data/61080005-8d6d-82b8-614a-1c8cb0f8dcc6.txt)

Messages when health monitor is opened are [here](./data/61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.05.txt) this was recorded on 29.3.2024 around 17:05, with heart rate being 75 at start going to 101 and back to 75, each log is about a second apart. and there is another log [here](./data/61080005-8d6d-82b8-614a-1c8cb0f8dcc6-health-monitor-29.3.17.22.txt) recorded at 17:22, with heart rate being around 78.

See [here](./misc.py) for more function of decoding.

#### WHOOP_CHAR_MEMFAULT 61080007-8d6d-82b8-614a-1c8cb0f8dcc6

-||-

## Notes

- As it is well known device broadcasts data to phone which sends it to servers which give all metrics, but I am not sure in which way is it done, that is, is mobile phone just a proxy which passes data from band to servers, or does phone do some decoding, if phone decodes data before sending it to server some of data could be reverse engineered from apk

- I think that sleep detection is done on phone, where it detects periods where phone is not being used and checks if heart rate, Sp02 and temperature correspond, reason why I think this is that it has detected few naps while I was working, my RHR is 55-ish and my heart rate when working is 60-ish (I work as dev).

- As mentioned above, there seem to be some problems if device is shoving Sp02 for 24h/7, but I think that is still being broadcasted all the time to calculate rest.

- It seems that on some packages that are 2 timestamps, or duration and timestamp, I think that this is how 24h heart rate is transferred to phone/servers

- Sleep performance: I think this is just duration of actual sleep, compared to recommended duration, my REM and deep sleep are almost always exact percentage so I might be wrong.

## Opcodes

These are package opcodes:

```
{
    "0x12": 258,
    "0x52": 2732,
    "0x1b": 127898,
    "0x1d": 7
}
```

All packages with opcode `0x1d` have following data: `0100ffff`. All packages with opcode `0x12` and `0x52` are write packages, packages with opcode `0x1b` are read packages.

Packages with opcode `0x52` and size `0x48` is used to send command to device, in [`misc.py`](./misc.py) function `decode_48` is used to decode.

Packages with opcode `0x52` and size `0x08` is used to trigger whoop, and whoop then sends data on [#WHOOP_CHAR_CMD_FROM_STRAP](#whoop_char_cmd_from_strap-61080003-8d6d-82b8-614a-1c8cb0f8dcc6) and on [#WHOOP_CHAR_DATA_FROM_STRAP](#whoop_char_data_from_strap-61080005-8d6d-82b8-614a-1c8cb0f8dcc6)

Packages with opcode `0x52` and size `0x10` seem to be used for setting alarm, but not fully sure

I have no idea for what packages with size `0x8c` are used for or what they are