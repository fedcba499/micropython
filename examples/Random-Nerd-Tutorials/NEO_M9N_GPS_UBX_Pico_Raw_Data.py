from machine import UART
import struct
import time

# Initialize UART1 (pins depend on your board, e.g., ESP32/Pico)
uart = UART(1, baudrate=115200, tx=4, rx=5) 

def get_ubx_pvt():
    # 1. Look for UBX Sync Chars (0xB5 0x62)
    if uart.any() >= 100:
        if uart.read(1) == b'\xb5':
            if uart.read(1) == b'\x62':
                # 2. Read Class (0x01), ID (0x07), and Length (0x5C 0x00 = 92)
                header = uart.read(4)
                if header[:2] == b'\x01\x07':
                    # 3. Read the 92-byte payload + 2-byte checksum
                    payload = uart.read(92)
                    checksum = uart.read(2)
                    
                    # 4. Parse specific offsets using struct.unpack
                    # < = Little Endian
                    # i = int32 (4 bytes), I = uint32 (4 bytes)
                    # Offsets below are relative to the start of the 92-byte payload
                    
                    # Longitude: Offset 24, Latitude: Offset 28
                    lon_raw = struct.unpack("<i", payload[24:28])[0]
                    lat_raw = struct.unpack("<i", payload[28:32])[0]
                    
                    # Horizontal Accuracy (hAcc): Offset 40
                    hacc_raw = struct.unpack("<I", payload[40:44])[0]
                    
                    # 5. Check Fix Status (Offset 21, bit 0)
                    flags = payload[21]
                    gnss_fix_ok = flags & 0x01
                    
                    if gnss_fix_ok:
                        lat = lat_raw / 1e7
                        lon = lon_raw / 1e7
                        hacc_m = hacc_raw / 1000.0 # Convert mm to meters
                        
                        return lat, lon, hacc_m
    return None

while True:
    # Clear the buffer
    # Read everything currently in the 'waiting room and throw it away
    if uart.any() > 0:
        uart.read()

    # Wait for a fresh message
    # Since we just cleared the buffer, we have to wait a tiny bit
    # for a brand new, current message to arrive from the GPS.
    # At 10Hz, a new message arrives every 100ms.

    pos = None
    timeout = 200 # ms
    start = time.ticks_ms()

    while pos is None and time.ticks_diff(time.ticks_ms(), start) < timeout:
        pos = get_ubx_pvt()

    if pos:
        print("Lat: {:.7f}, Lon: {:.7f}, Accuracy: {:.2f}m".format(*pos))
        
    time.sleep(0.1)