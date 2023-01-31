import draw
from dates import day_str, mon_str, week_of_year, day_of_week
from urllib import urequest
import gc
import ujson
from secrets import FUNCTION_URL
from inky_helper import today

def get_agenda():
    print("GET_AGENDA")
    today()
    #gc.collect()
    print("FREE")
    try:
        # Grab the data
        print(FUNCTION_URL)
        socket = urequest.urlopen(FUNCTION_URL)
        print("JSON")
        j = ujson.load(socket)
        socket.close()
        print(j)
        gc.collect()
        return j
    except OSError as e:
        print(e)
    print("ERROR")
    return []

BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

AGENDA = [
    {"start": "All Day", "end": "", "description": "All day event", "colour": BLUE},
    {"start": "All Day", "end": "", "description": "All day event", "colour": RED},
    {"start": "08:00 - 10:00", "end": "10:00", "description": "Morning things", "colour": GREEN},
    {"start": "19:00 - 21:00", "end": "21:00", "description": "An evening activity", "colour": ORANGE},
    {"start": "Tomorrow", "end": "", "description": "Another event", "colour": WHITE}
]

def draw_agenda_items(display, DATE, TODAY, items = AGENDA):
    print("DRAW_AGENDA_ITEMS")
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
        draw.outline(display, description_x, offset_y, 600 - description_x - 2*spacing, item_height - 2*spacing, spacing, item["colour"], item["colour"])
        display.set_pen(TAUPE)
        display.text(item["description"], description_x, offset_y, 600 - description_x, descr_size)

def draw_agenda(display, DATE, TODAY):
    print("DRAW_AGENDA")
    display.set_pen(WHITE)
    display.clear()
    dow = day_of_week(DATE["year"], DATE["month"], DATE["day"])
    draw.title(display, day_str(dow) + " " + str(DATE["day"]) + "th " + mon_str(DATE["month"]) + " " + str(DATE["year"]) + " - Week " + str(week_of_year(DATE["year"], DATE["month"], DATE["day"])))
    draw.nav(display, (("Prev", 30, False), ("Agenda", 10, False), ("TODAY", 20, False), ("Month", 17, True), ("Next", 29, False)))
    # get_calendar()
    items = get_agenda()
    print(items)
    draw_agenda_items(display, DATE, TODAY, items)
    draw.time(display, TODAY)
    draw.update(display)
