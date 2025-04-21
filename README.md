# pinball-nudge-controller
A accelerometer based nudge solution for a virtual pinball using a ADXL335B and a Raspberry Pi Pico

Download a ZIP of all these files.
Install CircuitPython 9 onto your Pico 2040
Basically copy over all the files and folders

Wire X from ADXL335B to A1 (27)
Wire Y from ADXL335B to A2 (28)
Wire GND to GND
and 3V to VCC on the ADXL335B

Boot her up. You'll see a CircuitPython HID in "Set Up USB Game Controllers"

If you want to change the sensitivity , 
