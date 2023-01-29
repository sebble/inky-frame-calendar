ROTATE=0

from picographics import PicoGraphics, DISPLAY_INKY_FRAME
display = PicoGraphics(display=DISPLAY_INKY_FRAME, rotate=ROTATE)
from urllib import urequest
import time
import network
import secrets
import gc

def init():
    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    
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
    {"start": "All Day", "end": "", "description": "Mum Away", "colour": BLUE},
    {"start": "All Day", "end": "", "description": "Lol Birthday", "colour": RED},
    {"start": "08:00 - 10:00", "end": "10:00", "description": "Morning things", "colour": GREEN},
    {"start": "19:00 - 21:00", "end": "21:00", "description": "Drumming", "colour": ORANGE},
    {"start": "Tomorrow", "end": "", "description": "Seb in Newcastle", "colour": WHITE}
]

print("starting...")

def read_until(stream, char):
    result = b""
    while True:
        c = stream.read(1)
        if c == char:
            return result
        result += c


def discard_until(stream, c):
    while stream.read(1) != c:
        pass

def parse_ical_feed(s, start_date = (2023,01,01), max_items = 10):
    events = []
    while True:
        char = s.read(1)
        if len(char) == 0:
            break
        
        discard_until(s, b"\n")
        field = read_until(s, b":")
        value = read_until(s, b"\n")
        
        print([field, value])
        gc.collect()


# import ssl
# scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

def get_ical(url):
    print("get")
    try:
        print("try")
        stream = urequest.urlopen(url, context=scontext)
        print("stream")
        output = list(parse_ical_feed(stream))
        print("output")
        return output

    except OSError as e:
        print(e)
        return False

def draw_agenda_items(items = AGENDA):
    last_start = ""
    date_x = 0
    date_y = 50
    date_size = 2
    description_x = 130
    item_height = 45
    descr_size = 4
    spacing = 8
    
    for i, item in enumerate(items):
        offset_y = i * (item_height+spacing) + date_y
        if last_start != item["start"]:
            last_start = item["start"]
            display.set_pen(BLACK)
            display.text(item["start"], date_x, offset_y, description_x, date_size)
        draw_outline(description_x, offset_y, 600 - description_x - 2*spacing, item_height - 2*spacing, spacing, item["colour"], item["colour"])
        display.set_pen(TAUPE)
        display.text(item["description"], description_x, offset_y, 600 - description_x, descr_size)
            

def draw_title(msg, offset = 0):
    display.set_pen(BLACK)
    display.text(msg, offset, 0, 600, 4)

def draw_outline(x, y, w, h, thickness = 3, colour = BLACK, fill = WHITE):
    display.set_pen(colour)
    display.rectangle(x - thickness, y - thickness, w + 2*thickness, h + 2*thickness)
    display.set_pen(fill)
    display.rectangle(x, y, w, h)

def draw_nav(buttons):
    pos_x = 0
    pos_y = 422
    font_size = 3
    draw_outline(250, 418, 100, 50)
    adjust_x = (23, 30, 16, 15, 29)
    # buttons = (("Prev", 30), ("Week", 30), ("TODAY", 20), ("Month", 17), ("Next", 29))
    for i, (label, adjust) in enumerate(buttons):
        offset_x = int(i * 600 / 5) + pos_x + adjust
        display.set_pen(BLACK)
        display.text(label, offset_x, pos_y, int(600 / 5), font_size)

DAY_TXT = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTH_TXT = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
MONTH_TXT2 = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

def draw_agenda():
    display.set_pen(WHITE)
    display.clear()
    draw_title(DAY_TXT[DATE["dow"]] + " " + str(DATE["day"]) + "th " + MONTH_TXT2[DATE["month"]] + " " + str(DATE["year"]) + " - Week 17")
    draw_nav((("Prev", 30), ("Week", 30), ("TODAY", 20), ("Month", 17), ("Next", 29)))
    # get_calendar()
    draw_agenda_items()
    display.update()

def get_calendar():
    res = get_ical(secrets.ICS_URL)
    print(res)

    
def draw_weekdays():
    col_width = int((600 - week_margin) / 7)
    font_size = 3
    if DATE["year"] == TODAY["year"] and DATE["month"] == TODAY["month"]:
        today = TODAY["dow"] # 0: Monday
    else:
        today = 9 # impossible value
    shift = 6
    for i, day in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        x = week_margin + i * col_width
        display.set_pen(BLACK)
        display.text(day, x, title_margin, col_width, font_size)
        if i == today:
            draw_outline(x, title_margin, 42, 26, shift, TAUPE, TAUPE)
            display.set_pen(BLACK)
            display.text(day, x, title_margin, col_width, font_size)

def draw_month_days():
    col_width = int((600 - week_margin) / 7)
    row_height = 50
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    if DATE["year"] == TODAY["year"] and DATE["month"] == TODAY["month"]:
        today = TODAY["day"] # 0: Monday
    else:
        today = 99 # impossible value
    month_start = day_of_week(DATE["year"], DATE["month"], 1)
    font_size = 5
    days = [""] * month_start + days + [""] * 14
    if DATE["year"] < TODAY["year"] or (DATE["month"] =< TODAY["month"]  and DATE["year"] >= TODAY["year"]):
        past = True
    else:
        past = False
    for row in (0, 1, 2, 3, 4, 5):
        y = title_margin*2 + row * row_height
        for col in (0, 1, 2, 3, 4, 5, 6):
            x = week_margin + col * col_width
            if today == days[row * 7 + col]:
                draw_outline(x - font_size, y - font_size, col_width - font_size, row_height - font_size, 0, BLACK, BLACK)
                display.set_pen(WHITE)
                past = False
            elif past:
                display.set_pen(TAUPE)
            else:
                display.set_pen(BLACK)
            display.text(str(days[row * 7 + col]), x, y, col_width, font_size)
        
        if str(days[row * 7]) != "" or str(days[row * 7 + 6]) != "":
            if row + 23 == 27:
                draw_outline(0, y, week_margin - 20, 24, 0, TAUPE, TAUPE)
            display.set_pen(BLACK)
            display.text("Wk " + str(row + 23), 0, y + 6, week_margin, 2)


def draw_month():
    display.set_pen(WHITE)
    display.clear()
    draw_title(MONTH_TXT[DATE["month"]] + " " + str(DATE["year"]), 150)
    draw_nav((("Prev", 30), ("Agenda", 10), ("TODAY", 20), ("Week", 30), ("Next", 29)))
    # get_calendar()
    draw_weekdays()
    draw_month_days()
    display.update()

def month_key(year, month):
    if month > 2:
        return [0, 0, 0, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6][month]
    elif year % 4 == 0:
        return [0, 0, 3][month]
    else:
        return [0, 1, 4][month]

def day_of_week(year, month, day):
    # Assume 2000 to 2099
    # Zero is Monday
    return (year % 100 + int(year % 100 / 4) + day + month_key(year, month) - 1 + 5) % 7

def get_today():
    import ntp
    date = ntp.fetch()
    print(date)
    gc.collect()
    return {"year": date[0], "month": date[1], "day": date[2], "dow": day_of_week(date[0], date[1], date[2])}


TODAY = get_today()
DATE = get_today()
print(DATE)
# draw_agenda()
draw_month()

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
