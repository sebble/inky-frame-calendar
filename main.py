# Configure your calendar here:
ROTATE=0 # 0 or 180
# ...

from secrets import ICS_URL, WIFI_PASSWORD, WIFI_SSID
import gc
import time
from dates import day_of_week, week_of_year, day_of_year
import draw
import ical
import month, agenda, week
import inky_helper
import wifi
import ntp
import app

time.sleep(0.5)

# wifi.init()

inky_helper.network_connect(WIFI_SSID, WIFI_PASSWORD)

BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7



print("starting...")

def get_calendar():
    res = get_ical(ICS_URL)
    print(res)

#TODAY = inky_helper.today()
#DATE = inky_helper.today()
#print(DATE)


# agenda.draw_agenda(display, DATE, TODAY)
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
        app.prev_page()
    elif inky_frame.button_b.read():
        inky_frame.button_b.led_on()
        app.view_agenda()
    elif inky_frame.button_c.read():
        inky_frame.button_c.led_on()
        app.today()
    elif inky_frame.button_d.read():
        inky_frame.button_d.led_on()
        app.view_month()
    elif inky_frame.button_e.read():
        inky_frame.button_e.led_on()
        app.next_page()

    
# inky_helper.sleep(10)
machine.reset()
