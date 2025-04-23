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

## this version below auto centres nd has tunables and is much more advnqaced.
##import time
##import board
##import analogio
##import usb_hid
##import struct
##
### Analog inputs from ADXL335 X and Y axes
##x_in = analogio.AnalogIn(board.A1)
##y_in = analogio.AnalogIn(board.A2)
##
##joystick = usb_hid.devices[0]
##
### Function to calibrate center positions
##def calibrate_center(pin, samples=100):
##    total = 0
##    for _ in range(samples):
##        total += pin.value
##        time.sleep(0.001)
##    return total / samples
##
##print("Calibrating...")
##x_center = calibrate_center(x_in)
##y_center = calibrate_center(y_in)
##print("Calibration complete.")
##
### TUNABLE SETTINGS
##DEAD_ZONE = 800                # Ignore small wobbles
##SENSITIVITY_MULTIPLIER = 5.0  # Higher = more sensitive
##ADC_MAX = 65535                # Analog-to-digital conversion max
##HID_MAX = 255                  # HID joystick max
##RECALIBRATION_INTERVAL = 4    # Seconds between recalibrations
##REPORT_INTERVAL = 0.01         # Seconds between reports sent
##CALIBRATION_SAMPLES = 100      # Number of samples for center calibration
##SMOOTHING_FACTOR = 0.1         # Smoothing applied to axis readings (lower is smoother)
##
### Function to read axis value with smoothing
##def read_axis(analogin, center, previous_value=None):
##    raw = analogin.value
##    delta = raw - center
##
##    # Apply dead zone
##    if abs(delta) < DEAD_ZONE:
##        delta = 0
##
##    # Amplify delta for sensitivity
##    delta *= SENSITIVITY_MULTIPLIER
##
##    # Clip to range before mapping
##    max_range = ADC_MAX / 2
##    delta = max(-max_range, min(max_range, delta))
##
##    # Normalize: scale -32768..+32767 to 0..255
##    scaled = int(((delta + max_range) / (ADC_MAX)) * HID_MAX)
##    scaled = max(0, min(HID_MAX, scaled))
##
##    # Apply smoothing (if a previous value exists)
##    if previous_value is not None:
##        scaled = int((previous_value * SMOOTHING_FACTOR) + (scaled * (1 - SMOOTHING_FACTOR)))
##
##    return scaled
##
### Main loop with periodic recalibration and additional tunables
##last_recalibration_time = time.monotonic()
##previous_x = None
##previous_y = None
##
##while True:
##    # Recalibrate the center periodically
##    if time.monotonic() - last_recalibration_time > RECALIBRATION_INTERVAL:
##        x_center = calibrate_center(x_in, CALIBRATION_SAMPLES)
##        y_center = calibrate_center(y_in, CALIBRATION_SAMPLES)
##        last_recalibration_time = time.monotonic()
##        print(f"Joystick recalibrated: x_center={x_center:.2f}, y_center={y_center:.2f}")
##
##    # Read axis values with smoothing and send joystick report
##    x = read_axis(x_in, x_center, previous_x)
##    y = read_axis(y_in, y_center, previous_y)
##    previous_x, previous_y = x, y
##
##    report = struct.pack("BB", x, y)
##    joystick.send_report(report)
##
##    time.sleep(REPORT_INTERVAL)
##
##
