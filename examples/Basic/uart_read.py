from machine import UART, Pin
import time

# UART0 on GP0 (TX) and GP1 (RX)
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

print("Listening on RX...")

while True:
    if uart.any():
        data = uart.read()
        print("Received:", data)
    time.sleep(0.1)
