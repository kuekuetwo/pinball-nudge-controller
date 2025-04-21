# Pinball Nudge Controller

An accelerometer-based nudge solution for virtual pinball using an ADXL335B and a Raspberry Pi Pico.

## Steps to Get Started

1. **Download** a ZIP file containing all necessary files.
2. **Install CircuitPython 9** onto your Pico 2040.
3. **Copy Over Files**: Transfer all files and folders onto your device.

## Wiring Instructions

| ADXL335B       | PICO            |
|----------------|-----------------|
| X AXIS         | A1 (Pin 27)     |
| Y AXIS         | A2 (Pin 28)     |
| GND            | GND             |
| VCC            | 3V              |

## Booting Up

Once everything is wired and set up:
- Boot the Raspberry Pi Pico.
- You'll see a **CircuitPython HID device** listed under "Set Up USB Game Controllers."

## Adjusting Sensitivity

If you need to change the sensitivity:
- Modify the corresponding parameters in the provided files.

---

Ready to bring your virtual pinball game to life? Let me know if you'd like more details or assistance! 🚀
