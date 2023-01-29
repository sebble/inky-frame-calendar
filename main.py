# Configure your calendar here:
ROTATE=0 # 0 or 180
# ...

from picographics import PicoGraphics, DISPLAY_INKY_FRAME
display = PicoGraphics(display=DISPLAY_INKY_FRAME, rotate=ROTATE)
from urllib import urequest
import time
import network
from secrets import WIFI_PASSWORD, WIFI_SSID, ICS_URL
import gc
from dates import day_of_week
import draw
import ical
import month, agenda, week

def init():
    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Wait for connect success or failure
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed %d' % wlan.status())
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

init()

BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

week_margin = 80
title_margin = 50

display.set_font("bitmap8")

AGENDA = [
    {"start": "All Day", "end": "", "description": "All day event", "colour": BLUE},
    {"start": "All Day", "end": "", "description": "All day event", "colour": RED},
    {"start": "08:00 - 10:00", "end": "10:00", "description": "Morning things", "colour": GREEN},
    {"start": "19:00 - 21:00", "end": "21:00", "description": "An evening activity", "colour": ORANGE},
    {"start": "Tomorrow", "end": "", "description": "Another event", "colour": WHITE}
]

print("starting...")

def get_calendar():
    res = get_ical(ICS_URL)
    print(res)

    

def get_today():
    import ntp
    date = ntp.fetch()
    print(date)
    gc.collect()
    return {"year": date[0], "month": date[1], "day": date[2], "dow": day_of_week(date[0], date[1], date[2])}


TODAY = get_today()
DATE = get_today()
print(DATE)
# agenda.draw_agenda()
month.update()

from pimoroni import ShiftRegister
from machine import Pin

# Inky Frame uses a shift register to read the buttons
SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10

sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)
# set up the button LEDs
button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)

while True:
    button_a_led.off()
    button_b_led.off()
    button_c_led.off()
    button_d_led.off()
    button_e_led.off()

    # read the shift register
    # we can tell which button has been pressed by checking if a specific bit is 0 or 1
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]

    if button_a == 1:
        button_a_led.on()
        if DATE["month"] == 1:
            DATE["year"] -= 1
            DATE["month"] = 12
        else:
            DATE["month"] -= 1
        draw_month()
    elif button_b == 1:
        button_b_led.on()
    elif button_c == 1:
        button_c_led.on()
        DATE = get_today()
        draw_month()
    elif button_d == 1:
        button_d_led.on()
    elif button_e == 1:
        button_e_led.on()
        if DATE["month"] == 12:
            DATE["year"] += 1
            DATE["month"] = 1
        else:
            DATE["month"] += 1
        draw_month()
