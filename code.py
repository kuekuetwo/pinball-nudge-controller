import time
import board
import analogio
import usb_hid
import struct

# Analog inputs from ADXL335 X and Y axes
x_in = analogio.AnalogIn(board.A1)
y_in = analogio.AnalogIn(board.A2)


joystick = usb_hid.devices[0]


def calibrate_center(pin, samples=100):
    total = 0
    for _ in range(samples):
        total += pin.value
        time.sleep(0.001)
    return total / samples

print("Calibrating...")
x_center = calibrate_center(x_in)
y_center = calibrate_center(y_in)
print("Calibration complete.")

#  TUNABLE SETTINGS
DEAD_ZONE = 500         # Ignore small wobbles
SENSITIVITY_MULTIPLIER = 8.0  # higher = more sensitive
ADC_MAX = 65535
HID_MAX = 255



def read_axis(analogin, center):
    raw = analogin.value
    delta = raw - center

    # Apply dead zone
    if abs(delta) < DEAD_ZONE:
        delta = 0

    # Amplify delta for sensitivity
    delta *= SENSITIVITY_MULTIPLIER

    # Clip to range before mapping
    max_range = ADC_MAX / 2
    delta = max(-max_range, min(max_range, delta))

    # Normalize: scale -32768..+32767 to 0..255
    scaled = int(((delta + max_range) / (ADC_MAX)) * HID_MAX)
    return max(0, min(HID_MAX, scaled))

while True:
    x = read_axis(x_in, x_center)
    y = read_axis(y_in, y_center)

    report = struct.pack("BB", x, y)
    joystick.send_report(report)

    time.sleep(0.01)

