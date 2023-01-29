
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
    display.update()
