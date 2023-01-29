import draw, dates
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

def draw_weekdays(display, DATE, TODAY):
    col_width = int((600 - week_margin) / 7)
    font_size = 3
    if DATE["year"] == TODAY["year"] and DATE["month"] == TODAY["month"]:
        today = dates.day_of_week(TODAY["year"], TODAY["month"], TODAY["day"]) # 0: Monday
    else:
        today = 9 # impossible value
    shift = 6
    for i, day in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        x = week_margin + i * col_width
        display.set_pen(BLACK)
        display.text(day, x, title_margin, col_width, font_size)
        if i == today:
            draw.outline(display, x, title_margin, 42, 26, shift, TAUPE, TAUPE)
            display.set_pen(BLACK)
            display.text(day, x, title_margin, col_width, font_size)

def draw_month_days(display, DATE, TODAY):
    col_width = int((600 - week_margin) / 7)
    row_height = 50
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    if DATE["year"] == TODAY["year"] and DATE["month"] == TODAY["month"]:
        today = TODAY["day"] # 0: Monday
    else:
        today = 99 # impossible value
    month_start = dates.day_of_week(DATE["year"], DATE["month"], 1)
    font_size = 5
    days = [""] * month_start + days + [""] * 14
    if DATE["year"] < TODAY["year"] or (DATE["month"] <= TODAY["month"]  and DATE["year"] >= TODAY["year"]):
        past = True
    else:
        past = False
    for row in (0, 1, 2, 3, 4, 5):
        y = title_margin*2 + row * row_height
        for col in (0, 1, 2, 3, 4, 5, 6):
            x = week_margin + col * col_width
            if today == days[row * 7 + col]:
                draw.outline(display, x - font_size, y - font_size, col_width - font_size, row_height - font_size, 0, BLACK, BLACK)
                display.set_pen(WHITE)
                past = False
            elif past:
                display.set_pen(TAUPE)
            else:
                display.set_pen(BLACK)
            display.text(str(days[row * 7 + col]), x, y, col_width, font_size)
        
        if str(days[row * 7]) != "" or str(days[row * 7 + 6]) != "":
            if row + 23 == 27:
                draw.outline(display, 0, y, week_margin - 20, 24, 0, TAUPE, TAUPE)
            display.set_pen(BLACK)
            if str(days[row * 7]) != "":
                display.text("Wk " + str(dates.week_of_year(DATE["year"], DATE["month"], days[row * 7])), 0, y + 6, week_margin, 2)
            elif str(days[row * 7 + 6]) != "":
                display.text("Wk " + str(dates.week_of_year(DATE["year"], DATE["month"], days[row * 7 + 6])), 0, y + 6, week_margin, 2)


def update(display, DATE, TODAY):
    display.set_pen(WHITE)
    display.clear()
    draw.title(display, dates.month_str(DATE["month"]) + " " + str(DATE["year"]), 150)
    draw.nav(display, (("Prev", 30, True), ("Agenda", 10, True), ("TODAY", 20, True), ("Month", 17, False), ("Next", 29, True)))
    # get_calendar()
    draw_weekdays(display, DATE, TODAY)
    draw_month_days(display, DATE, TODAY)
    draw.time(display, TODAY)
    draw.update(display)
