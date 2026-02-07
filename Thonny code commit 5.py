import network
import urequests
import time
from machine import Pin

WIFI_SSID = "Smth"
WIFI_PASSWORD = "System222"

BACKEND_URL = "http://10.17.33.88:8000/trigger" 

DEVICE_ID = "esp32_hackathon_1"
USER_ID = "default"

BUTTONS = {
    "BTN1": Pin(14, Pin.IN, Pin.PULL_UP),
    "BTN2": Pin(27, Pin.IN, Pin.PULL_UP),
    "BTN3": Pin(26, Pin.IN, Pin.PULL_UP),
    "BTN4": Pin(25, Pin.IN, Pin.PULL_UP),
    "BTN5": Pin(33, Pin.IN, Pin.PULL_UP),
    "BTN6": Pin(32, Pin.IN, Pin.PULL_UP),
}

last_state = {b: 1 for b in BUTTONS}
DEBOUNCE = 0.4

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(0.5)

    print("WiFi connected:", wlan.ifconfig())

def send_event(button):
    payload = {
        "button": button,
        "language": "en",
        "device_id": DEVICE_ID,
        "user_id": USER_ID
    }

    try:
        r = urequests.post(BACKEND_URL, json=payload)
        print("Sent", button, "→", r.status_code)
        r.close()
    except Exception as e:
        print("SERVER ERROR:", e)

connect_wifi()
print("\nDEVICE READY\n")

while True:
    for name, pin in BUTTONS.items():
        val = pin.value()

        if val == 0 and last_state[name] == 1:
            print("BUTTON PRESSED:", name)
            send_event(name)
            time.sleep(DEBOUNCE)

        last_state[name] = val

    time.sleep(0.05)