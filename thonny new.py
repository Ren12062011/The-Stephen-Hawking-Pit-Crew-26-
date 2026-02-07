Thonny new code:

import network
import urequests
import time
from machine import Pin
WIFI_SSID = "Smth"
WIFI_PASSWORD = "System222"

BOT_TOKEN = "8417493285:AAFQ6b8oR0qQlMI2vhxzGDLAATysrZAfC4Y"
CHAT_ID = "8106146605"

TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)

DEVICE_ID = "esp32_hackathon_1"

BUTTON_PINS = {
    "BTN1": Pin(14, Pin.IN, Pin.PULL_UP),
    "BTN2": Pin(27, Pin.IN, Pin.PULL_UP),
    "BTN3": Pin(26, Pin.IN, Pin.PULL_UP),
    "BTN4": Pin(25, Pin.IN, Pin.PULL_UP),
    "BTN5": Pin(33, Pin.IN, Pin.PULL_UP),
    "BTN6": Pin(32, Pin.IN, Pin.PULL_UP),
}

BUTTON_MESSAGES = {
    "BTN1": "I need immediate help.",
    "BTN2": "Please come here.",
    "BTN3": "I need water.",
    "BTN4": "I need food.",
    "BTN5": "I am not feeling well.",
    "BTN6": "EMERGENCY! Please call for help immediately."
}

last_state = {b: 1 for b in BUTTON_PINS}
DEBOUNCE = 0.4

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(0.5)

    print("WiFi connected:", wlan.ifconfig())

def send_telegram_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        r = urequests.post(TELEGRAM_URL, json=payload)
        print("Telegram response:", r.status_code)
        r.close()
    except Exception as e:
        print("Telegram error:", e)

connect_wifi()
send_telegram_message("Device {} is online and ready.".format(DEVICE_ID))
print("\nDEVICE READY\n")

while True:
    for btn_name, pin in BUTTON_PINS.items():
        val = pin.value()

        if val == 0 and last_state[btn_name] == 1:
            message = BUTTON_MESSAGES[btn_name]
            full_message = "{} (Device: {})".format(message, DEVICE_ID)

            print("BUTTON PRESSED:", btn_name, "→", message)
            send_telegram_message(full_message)

            time.sleep(DEBOUNCE)

        last_state[btn_name] = val

    time.sleep(0.05)
