# IoT_Flood_Monitoring_System
Real time water level monitoring system using Raspberry Pi Pico for flood_prone areas

## Group Members
- **Sakshath S Shetty** NNM23EC149 [sakshathshetty05]
- **Samarth D Prabhu** NNM23EC151 [eceai]
- **Shamith Hegde** NNM23EC159 [hegde05]

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
    A([Start]) --> B["Init Pins: Buzzer=OFF, Alert LED=OFF"]
    B --> C["connect_wifi()"]
    C --> D["get_chat_id()"]
    D --> E("Start: while True loop")
    E --> F["dist = get_distance()"]
    F --> G{"Is dist valid?"}
    
    %% Path if Sensor Fails
    G -- No --> H["Print: Sensor error..."]
    H --> X["Time.sleep(7)"]

    %% Path if Sensor Works
    G -- Yes --> I["Store Reading (Timestamp & Level)"]
    I --> J["Calculate fill_percent"]
    J --> K{"Is level < 10cm (ALERT)?"}
    
    %% === ALERT STATE BRANCH (DANGER) ===
    K -- Yes --> L["Set Pins: Alert LED=1 (ON), Buzzer=0 (ON)"]
    L --> M{"Have 2 readings to compare?"}
    
    %% New Overflow Logic Feature
    M -- Yes --> N["Calculate Rise Rate (cm/sec)"]
    N --> O["Calculate Estimated Time to Overflow"]
    O --> P["Add Estimation to Telegram Message"]
    M -- No --> Q["Prepare Basic Alert Message"]
    P --> Q
    
    Q --> R["telegram_send(message)"]
    R --> S["last_state = ALERT"]
    
    %% === SAFE STATE BRANCH ===
    K -- No --> T["Set Pins: Alert LED=0 (OFF), Buzzer=1 (OFF)"]
    T --> U{"If last_state != SAFE?"}
    U -- Yes --> V["telegram_send(Safe Message)"]
    V --> W["last_state = SAFE"]
    U -- No --> W

    %% Join branches to send data to cloud
    S --> Z["send_data(dist) to ThingSpeak"]
    W --> Z
    
    %% Loop back
    Z --> X
    X --> E
