
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
        draw.outline(description_x, offset_y, 600 - description_x - 2*spacing, item_height - 2*spacing, spacing, item["colour"], item["colour"])
        display.set_pen(TAUPE)
        display.text(item["description"], description_x, offset_y, 600 - description_x, descr_size)

def draw_agenda():
    display.set_pen(WHITE)
    display.clear()
    draw.title(day_str(DATE["dow"]) + " " + str(DATE["day"]) + "th " + mon_str(DATE["month"]) + " " + str(DATE["year"]) + " - Week 17")
    draw.nav((("Prev", 30), ("Week", 30), ("TODAY", 20), ("Month", 17), ("Next", 29)))
    # get_calendar()
    draw_agenda_items()
    draw.time(display, TODAY)
    display.update()
