# 🔌 Wiring Connections

This document details the pin connections between the Raspberry Pi Pico W and the components.

## 1. HC-SR04 Ultrasonic Sensor
| Sensor Pin | Pico Pin | Description |
| :--- | :--- | :--- |
| **VCC** | **3.3V** | 5V Power Supply |
| **GND** | **GND** | Ground |
| **TRIG** | **GP28** | Trigger Signal |
| **ECHO** | **GP6** | Echo Signal |

## 2. Output Components
| Component | Component Leg | Pico Pin | Note |
| :--- | :--- | :--- | :--- |
| **Safe LED** | Anode (+) | **GP8** | Connected via Resistor |
| **Safe LED** | Cathode (-) | **GND** | Common Ground |
| **Buzzer** | Positive (+) | **GP13** | Signal |
| **Buzzer** | Negative (-) | **GND** | Common Ground |

*Note: The breadboard power rails are connected to VBUS (Red Rail) and GND (Blue Rail).*
