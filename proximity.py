# Sensor - HC SR04

from machine import Pin, time_pulse_us
import time

# Pin definitions
TRIG_PIN = 15  # Trigger pin
ECHO_PIN = 14  # Echo pin
LED_PIN = 13   # LED pin
BUTTON_PIN = 12  # Button pin

# Setup pins
trigger = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Ensure trigger is low
trigger.low()
led.low()

def measure_distance():
    """Measure distance in centimeters using HC-SR04"""
    # Send 10us pulse to trigger
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    
    # Measure echo pulse duration
    try:
        duration = time_pulse_us(echo, 1, 30000)  # 30ms timeout
        if duration < 0:
            return -1  # Timeout
        
        # Calculate distance (speed of sound = 343 m/s)
        # Distance = (duration * 0.0343) / 2
        distance = (duration * 0.0343) / 2
        return distance
    except:
        return -1

print("HC-SR04 Distance Sensor Ready")
print("Press button to start monitoring...")

sensor_active = False

while True:
    # Check button press (active low with pull-up)
    if button.value() == 0:  # Button pressed
        sensor_active = True
        print("Sensor activated!")
        time.sleep(0.3)  # Debounce
    
    if sensor_active:
        distance = measure_distance()
        
        if distance > 0:
            print(f"Distance: {distance:.1f} cm")
            
            # Check if distance is less than 50 cm
            if distance < 50:
                led.high()
                print("LED ON - Object detected!")
            else:
                led.low()
        else:
            print("Measurement error")
            led.low()
        
        time.sleep(0.1)  # Measure every 100ms
    else:
        led.low()
        time.sleep(0.1)