# 🔭 Scope of the Solution

## 1. Project Overview
The **IoT Flood Monitoring System** is designed to provide real-time water level data and automated alerts for flood-prone areas. By leveraging the Raspberry Pi Pico W, the system offers a low-cost, scalable solution for early disaster warning.

## 2. Functional Scope
The system is capable of the following functions:
* **Real-Time Monitoring:** Continuously measures the distance from the sensor to the water surface using ultrasonic technology.
* **Automated Alerting:**
    * **Safe State Indicator:** An LED remains **ON** to indicate the system is powered and water levels are safe.
    * **Danger Alert:** When water rises above the safety threshold, the **LED turns OFF** and the **Buzzer turns ON** immediately.
    * **Remote Notification:** Instant alerts are sent to a Telegram group via WiFi during danger conditions.
* **Cloud Analytics:** Uploads sensor data to the **ThingSpeak** IoT dashboard for historical analysis and visualization.
* **Overflow Estimation:** Calculates the estimated time until the dam overflows based on the rate of rising water.

## 3. Limitations
* **Connectivity:** The remote alerting and dashboard features require an active 2.4GHz WiFi connection.
* **Power Supply:** The system requires a continuous 5V power source (USB or Battery).
* **Sensor Range:** The ultrasonic sensor is effective within a specific range (2cm to 400cm).

---

# 🛠️ Required Components

To replicate this solution, the following hardware and software components are required.

## A. Hardware Requirements
| Component | Quantity | Description |
| :--- | :--- | :--- |
| **Raspberry Pi Pico W** | 1 | Microcontroller with built-in WiFi support. |
| **HC-SR04 Ultrasonic Sensor** | 1 | Measures distance/water level. |
| **Active Buzzer** | 1 | Provides audio alarm for critical status. |
| **LED (White/Green)** | 1 | Visual indicator for "Safe" status. |
| **Resistor (220Ω or 330Ω)** | 1 | Current limiting for the LED. |
| **Jumper Wires** | 1 Set | Male-to-Male / Male-to-Female wires. |
| **Micro-USB Cable** | 1 | For power and programming. |

## B. Software & IDE Requirements
* **Integrated Development Environment (IDE):**
    * **Thonny IDE:** Used for writing and uploading code to the Pico.
* **Firmware:**
    * **MicroPython:** The runtime environment installed on the Pico W.
* **Cloud & API Services:**
    * **ThingSpeak:** IoT analytics platform for the dashboard.
    * **Telegram Bot API:** Service for sending remote alert notifications.
