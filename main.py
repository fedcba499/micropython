import machine
import uos
import sdcard

# SPI setup (example using SPI0)
spi = machine.SPI(
    0,
    sck=machine.Pin(2),
    mosi=machine.Pin(3),
    miso=machine.Pin(4),
    baudrate=1_000_000
)

# Chip select pin
cs = machine.Pin(5, machine.Pin.OUT)

# Initialise SD card
sd = sdcard.SDCard(spi, cs)

# Format (ERASES everything!)
# uos.VfsFat.mkfs(sd)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Write a file on SD
with open("/sd/hello.txt", "w") as f:
    f.write("Hello from Pico 12!\r\n")

# Read the file back
with open("/sd/hello.txt", "r") as f:
    print("SD content:", f.read())
