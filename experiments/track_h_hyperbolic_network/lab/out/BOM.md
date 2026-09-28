# Bill of materials (two boards + calibration cells + measurement chain)

| Item | Qty | Spec | Note |
|---|---|---|---|
| Resistor 100 kOhm | 342 + 10 spare | metal film, 1 % (5 % acceptable for the differential tests, 1 % for tau) | 140 for {7,3} L=2, 200 for square R=6, 2 for calibration cells |
| Capacitor 1 uF | 106 + 6 spare | film (PET/PP) or C0G; NOT class-2 ceramic (DC bias), NOT electrolytic (leakage) | 35 + 69 interior nodes, 2 calibration cells |
| Perfboard / stripboard | 2 | >= 15 x 15 cm | one per board; or a 3D-printed jig following the schematic layout |
| Bus wire | 3 m | tinned copper | boundary rail and ground |
| Op-amp | 1 x quad | rail-to-rail input, low bias (MCP6004 / TLV2374 class) | unity-gain buffers: 1 driver + 3 probes |
| ADC | 1 | >= 12 bit with <= 1 LSB noise, >= 100 S/s per channel; 16-bit ADS1115 (860 SPS) recommended | the ESP32 internal ADC (10-bit effective) is EXCLUDED: the virtual bench gives +20 % to +80 % tau error with it |
| Microcontroller | 1 | ESP32 / Arduino / Raspberry Pi Pico | step generation (GPIO -> driver buffer), ADC readout, timestamping |
| DMM | 1 | 4.5 digits preferred | component sorting, static effective-resistance checks |
| Bench supply / USB 5 V | 1 | 3.3 V rail for the step | |
| Calibration cell | 2 | one R + one C from the same batches, on each board | measures RC directly: the tau predictions are multiples of it |

Nominal RC = 0.100 s; predicted tau: {7,3} L=2 = 0.275 s, square R=6 = 0.455 s; ratio 0.604.

Every row of a wiring table should be checked with the DMM before the next row is soldered.
