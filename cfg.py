#!/usr/bin/env python3

import sys
import hid # pip install hidapi
from struct import pack

VENDOR_ID = 0x2f68 
PRODUCT_ID = 0x0082 # DURGOD Taurus K320:
TIMEOUT = 200

deviceCfg = next(device for device in hid.enumerate() if device['vendor_id'] == VENDOR_ID and device['product_id'] == PRODUCT_ID and device['interface_number'] == 2 )

device = hid.device()
device.open_path(deviceCfg['path'])

PING    = b"\x00\x03\x07\xE3".ljust(64, b"\x00")
RESET   = b"\x00\x03\x05\x80\x04\xff".ljust(64, b"\x00")
SAVE    = b"\x00\x03\x05\x82".ljust(64, b"\x00")

keymap = [
b"\x00\x00\x00\x00\x00\x29\x00\x00\x00\x89\x00\x00\x00\x3a\x00\x00\x00\x3b\x00\x00\x00\x3c\x00\x00\x00\x3d\x00\x00\x00\x3e\x00\x00\x00\x3f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x40\x00\x00\x00\x41\x00\x00\x00\x42\x00\x00\x00\x43\x00\x00\x00\x44\x00\x00\x00\x45\x00\x00\x00\x46\x00\x00\x00\x47\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x48\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x35\x00\x00\x00\x1e\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x20\x00\x00\x00\x21\x00\x00\x00\x22\x00\x00\x00\x23\x00\x00\x00\x24\x00\x00\x00\x25\x00\x00\x00\x26\x00\x00\x00\x27\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x2d\x00\x00\x00\x2e\x00\x00\x00\x2a\x00\x00\x00\x49\x00\x00\x00\x4a\x00\x00\x00\x4b\x00\x00\x00\x53\x00\x00\x00\x54\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x55\x00\x00\x00\x56\x00\x00\x00\x2b\x00\x00\x00\x14\x00\x00\x00\x1a\x00\x00\x00\x08\x00\x00\x00\x15\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x18\x00\x00\x00\x0c\x00\x00\x00\x12\x00\x00\x00\x13\x00\x00\x00\x2f\x00\x00\x00\x30\x00\x00\x00\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x4c\x00\x00\x00\x4d\x00\x00\x00\x4e\x00\x00\x00\x5f\x00\x00\x00\x60\x00\x00\x00\x61\x00\x00\x00\x57\x00\x00\x00\x39\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",

b"\x00\x00\x00\x00\x00\x04\x00\x00\x00\x16\x00\x00\x00\x07\x00\x00\x00\x09\x00\x00\x00\x0a\x00\x00\x00\x0b\x00\x00\x00\x0d\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x33\x00\x00\x00\x34\x00\x00\x00\x32\x00\x00\x00\x28\x00\x00\x00\x4c\x00\x00\x00\x4d\x00\x00\x00\x4e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x5c\x00\x00\x00\x5d\x00\x00\x00\x5e\x00\x00\x00\x85\x00\x00\x00\xe1\x00\x00\x00\x64\x00\x00\x00\x1d\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x06\x00\x00\x00\x19\x00\x00\x00\x05\x00\x00\x00\x11\x00\x00\x00\x10\x00\x00\x00\x36\x00\x00\x00\x37\x00\x00\x00\x38\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x87\x00\x00\x00\xe5\x00\x00\x00\x00\x00\x00\x00\x52\x00\x00\x00\x00\x00\x00\x00\x59\x00\x00\x00\x5a\x00\x00\x00\x5b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x00\x00\x00\xe3\x00\x00\x00\xe2\x00\x00\x00\x8b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8a\x00\x00\x00\x88\x00\x00\x00\xe6\x00\x01\x00\x00\x00\x00\x00\xe7\x00\x00\x00\xe4\x00\x00\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
b"\x00\x00\x00\x00\x00\x51\x00\x00\x00\x4f\x00\x00\x00\x00\x00\x00\x00\x62\x00\x00\x00\x63\x00\x00\x00\x58\x00\x00\x00\x00\x00\x78\x56\x34\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
]

def send(data):
    print("->", data)
    if device.write(data) < 0: 
        raise "Write failed"

    resp = device.read(64, timeout_ms=500)
    print("<-", ' '.join(map(hex, resp)))


send(PING)
send(RESET)

for i, d in enumerate(keymap):
    print(i)
    send(b''.join([b"\x00\x03\x05\x81\x0f", pack('b', i), d]))

send(SAVE)
send(PING)

device.close()
