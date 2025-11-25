# IoT_Flood_Monitoring_System
Real time water level monitoring system using Raspberry Pi Pico for flood_prone areas

## Group Members
- **Sakshath S Shetty** NNM23EC149
- **Samarth D Prabhu** NNM23EC151
- **Shamith Hegde** NNM23EC159
===

### I. Problem Statement
Develop an IoT Flood Monitoring System with Raspberry Pi Pico for real-time water level monitoring and timely alerts

Flooding poses a significant and recurring risk in low-lying coastal regions. This project addresses the critical need for a **cost-effective and reliable real-time water level monitoring system** using the Raspberry Pi Pico to provide early warning, allowing local communities and authorities adequate time to prepare and mitigate disaster risks.

===

### V. Code Logic and Implementation

Our solution employs the MicroPython environment on the Raspberry Pi Pico W to continuously measure and monitor the water level. The core logic involves a repetitive cycle of distance measurement, state evaluation against predefined thresholds, and data transmission.

**The Logic Flow of `main.py`:**

```mermaid
%%{init: {'theme': 'neutral' } }%%
graph TD
    A([Start]) --> B["connect_wifi()"]
    B --> C["get_chat_id()"]
    C --> D("Start: while True loop")
    D --> E["dist = get_distance()"]
    E --> F{"Is dist valid?"}
    
    %% Path if Sensor Fails
    F -- No --> G["Print: Sensor error..."]
    G --> J["Time.sleep(7)"]

    %% Path if Sensor Works (Alert System Logic)
    F -- Yes --> K["Calculate level_cm & fill_percent"]
    K --> L{"Is level_cm < 20cm (CRITICAL)?"}
    
    %% Critical Branch
    L -- Yes --> M["Turn ON Red LED & Buzzer"]
    M --> O{"If last_state != CRITICAL?"}
    O -- Yes --> P["telegram_send(CRITICAL)"]
    P --> Q["last_state = CRITICAL"]
    O -- No --> Q
    
    %% Warning Branch
    L -- No --> S{"Is level_cm < 40cm (WARNING)?"}
    S -- Yes --> T["Turn ON Yellow LED & OFF Buzzer"]
    T --> V{"If last_state != WARNING?"}
    V -- Yes --> W["telegram_send(WARNING)"]
    W --> X["last_state = WARNING"]
    V -- No --> X

    %% Safe Branch
    S -- No --> Y["Turn OFF Yellow LED & Buzzer"]
    Y --> Z{"If last_state != SAFE?"}
    Z -- Yes --> B1["telegram_send(SAFE)"]
    B1 --> C1["last_state = SAFE"]
    Z -- No --> C1
    
    %% All branches go to Send Data
    Q --> I["send_data(dist) to ThingSpeak"]
    X --> I
    C1 --> I
    
    %% Loop back
    I --> J
    J --> D
