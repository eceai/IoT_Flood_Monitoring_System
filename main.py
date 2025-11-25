from machine import Pin, time_pulse_us
import time
import network
import urequests


# -------------------------------
# WIFI + THINGSPEAK SETTINGS
# -------------------------------
SSID = "Swasthik"
PASSWORD = "12345671"
API_KEY = "3AT4JNZONSUYMCI7"
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key=" + API_KEY

# -------------------------------
# TELEGRAM SETTINGS
# -------------------------------
TELEGRAM_TOKEN = "8347425872:AAEoi2VednRKrQdWFDKIvUBFg4GFcVcuHlY"
TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN
CHAT_ID = ""  # Auto-detected

# -------------------------------
# SENSOR & OUTPUT PINS
# -------------------------------
TRIG = Pin(28, Pin.OUT)
ECHO = Pin(6, Pin.IN)
buzzer = Pin(13, Pin.OUT)
led_safe = Pin(8, Pin.OUT)

# Initialize pins
# Buzzer is active LOW (0=ON, 1=OFF) based on your code logic
buzzer.value(1)       # OFF
led_safe.value(1)     # ON (System starts in SAFE mode)

# -------------------------------
# DAM SETTINGS
# -------------------------------
DAM_DEPTH_CM = 500  # Maximum dam depth in cm
ALERT_THRESHOLD_CM = 10  # ALERT level

# -------------------------------
# WIFI CONNECT
# -------------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nConnected! IP:", wlan.ifconfig()[0])
    return wlan

# -------------------------------
# TELEGRAM CHAT ID AUTO-DETECT
# -------------------------------
def get_chat_id():
    global CHAT_ID
    try:
        r = urequests.get(TELEGRAM_URL + "/getUpdates")
        data = r.json()
        r.close()
        if len(data["result"]) > 0:
            CHAT_ID = data["result"][0]["message"]["chat"]["id"]
            print("Detected TELEGRAM CHAT_ID:", CHAT_ID)
    except:
        print("Cannot detect chat ID.")

# -------------------------------
# TELEGRAM SEND
# -------------------------------
def telegram_send(text):
    global CHAT_ID
    if CHAT_ID == "":
        get_chat_id()
        if CHAT_ID == "":
            print("Telegram cannot send: No chat ID yet.")
            return
    try:
        url = TELEGRAM_URL + "/sendMessage"
        payload = "chat_id={}&text={}".format(CHAT_ID, text)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = urequests.post(url, data=payload, headers=headers)
        r.close()
    except Exception as e:
        print("Telegram Send Error:", e)

# -------------------------------
# ULTRASONIC SENSOR
# -------------------------------
def get_distance():
    TRIG.value(0)
    time.sleep_us(5)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    try:
        duration = time_pulse_us(ECHO, 1, 30000)
        distance = (duration * 0.0343) / 2
        if distance <= 0 or distance > DAM_DEPTH_CM:
            return None
        return distance
    except OSError:
        return None

# -------------------------------
# ALERT SYSTEM WITH STATE TRACKING & OVERFLOW ESTIMATION
# -------------------------------
last_state = None  # None, "SAFE", "ALERT"
last_readings = []  # To track last 2 readings with timestamp

def alert_system(level_cm):
    global last_state, last_readings

    timestamp = time.time()
    last_readings.append((timestamp, level_cm))
    if len(last_readings) > 2:
        last_readings.pop(0)

    fill_percent = (level_cm / DAM_DEPTH_CM) * 100
    message = ""

    if level_cm < ALERT_THRESHOLD_CM:  # ALERT (DANGER)
        led_safe.value(0)  # <--- OFF because it is DANGER
        buzzer.value(0)    # ON (Active Low)
        message = f"🚨 ALERT! Water Level = {level_cm:.2f} cm ({fill_percent:.1f}%)"

        # Estimate time to overflow if water is rising
        if len(last_readings) == 2:
            dt = last_readings[1][0] - last_readings[0][0]
            dh = last_readings[1][1] - last_readings[0][1]
            if dh > 0 and dt > 0:
                rate = dh / dt  # cm/sec
                remaining = DAM_DEPTH_CM - level_cm
                eta_sec = remaining / rate
                eta_min = eta_sec / 60
                message += f"\n⏱ Estimated time to overflow: {eta_min:.1f} min"

        print(f"ALERT! Water Level: {level_cm:.2f} cm ({fill_percent:.1f}%)")
        telegram_send(message)  # Send every reading during ALERT
        last_state = "ALERT"

    else:  # SAFE
        led_safe.value(1)  # <--- ON because it is SAFE
        buzzer.value(1)    # OFF (Active Low)
        print(f"Safe Level: {level_cm:.2f} cm ({fill_percent:.1f}%)")
        if last_state != "SAFE":
            telegram_send(f"✅ Water Level = {level_cm:.2f} cm ({fill_percent:.1f}%)")
            last_state = "SAFE"

def send_data(level_cm):
    try:
        url = f"{THINGSPEAK_URL}&field1={level_cm:.2f}"
        r = urequests.get(url)
        r.close()
        print(f"ThingSpeak OK: {level_cm:.2f} cm")
    except Exception as e:
        print("ThingSpeak Error:", e)

# -------------------------------
# MAIN PROGRAM
# -------------------------------
connect_wifi()
get_chat_id()

while True:
    dist = get_distance()
    if dist:
        alert_system(dist)
        send_data(dist)
    else:
        print("Sensor error or out of range")
    time.sleep(7)
