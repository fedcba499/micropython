from machine import UART
import struct
import time

uart = UART(1, baudrate=115200, tx=4, rx=5)

SYNC1 = 0xB5
SYNC2 = 0x62


def read_exact(n, timeout=200):
    """Read exactly n bytes or return None"""
    buf = b""
    t0 = time.ticks_ms()

    while len(buf) < n:

        if uart.any():
            data = uart.read(n - len(buf))
            if data:
                buf += data

        if time.ticks_diff(time.ticks_ms(), t0) > timeout:
            return None

    return buf


def read_ubx():

    while True:

        b = read_exact(1)
        if not b:
            return None

        if b[0] != SYNC1:
            continue

        b = read_exact(1)
        if not b or b[0] != SYNC2:
            continue

        cls = read_exact(1)
        mid = read_exact(1)

        if not cls or not mid:
            return None

        length_bytes = read_exact(2)
        if not length_bytes:
            return None

        length = struct.unpack('<H', length_bytes)[0]

        payload = read_exact(length)
        if not payload:
            return None

        checksum = read_exact(2)
        if not checksum:
            return None

        return cls[0], mid[0], payload


def get_int32_le(buf, offset):
    return struct.unpack_from('<i', buf, offset)[0]


while True:

    msg = read_ubx()

    if not msg:
        continue

    cls, mid, payload = msg

    # NAV-PVT
    if cls == 0x01 and mid == 0x07:

        # Safety check
        if len(payload) != 92:
            continue

        lon = get_int32_le(payload, 24) / 1e7
        lat = get_int32_le(payload, 28) / 1e7
        alt = get_int32_le(payload, 36) / 1000

        print("Lat:", lat)
        print("Lon:", lon)
        print("Alt:", alt, "m")
        print("----------------")

        time.sleep(1)
