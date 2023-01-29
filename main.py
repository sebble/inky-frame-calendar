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
from dates import day_of_week, week_of_year, day_of_year
import draw
import ical
import month, agenda, week
import inky_helper


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


display.set_font("bitmap8")

print("starting...")

def get_calendar():
    res = get_ical(ICS_URL)
    print(res)

    

def get_today():
    import ntp
    date = ntp.fetch()
    print(date)
    gc.collect()
    return {"year": date[0], "month": date[1], "day": date[2],
            "dow": day_of_week(date[0], date[1], date[2]),
            "week": week_of_year(date[0], date[1], date[2]),
            "doy": day_of_year(date[0], date[1], date[2]),
            "time": str(date[3]) + ":" + str(date[4])}


TODAY = get_today()
DATE = get_today()
print(DATE)
# agenda.draw_agenda()
# month.update(display, DATE, TODAY)

# TODO: check state file before updating screen
import inky_frame

while True:
    inky_frame.button_a.led_off()
    inky_frame.button_b.led_off()
    inky_frame.button_c.led_off()
    inky_frame.button_d.led_off()
    inky_frame.button_e.led_off()
    
    if inky_frame.button_a.read():
        inky_frame.button_a.led_on()
        if DATE["month"] == 1:
            DATE["year"] -= 1
            DATE["month"] = 12
        else:
            DATE["month"] -= 1
        month.update(display, DATE, TODAY)
    elif inky_frame.button_b.read():
        inky_frame.button_b.led_on()
    elif inky_frame.button_c.read():
        inky_frame.button_c.led_on()
        DATE = get_today()
        month.update(display, DATE, TODAY)
    elif inky_frame.button_d.read():
        inky_frame.button_d.led_on()
    elif inky_frame.button_e.read():
        inky_frame.button_e.led_on()
        if DATE["month"] == 12:
            DATE["year"] += 1
            DATE["month"] = 1
        else:
            DATE["month"] += 1
        month.update(display, DATE, TODAY)

    
# inky_helper.sleep(10)
machine.reset()
