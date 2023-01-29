import inky_helper
import month, agenda

from picographics import PicoGraphics, DISPLAY_INKY_FRAME
display = PicoGraphics(display=DISPLAY_INKY_FRAME, rotate=0)
display.set_font("bitmap8")

default_state = {
    "view": "month", # agenda
    "date": {"year": 1990, "month": 1, "day": 1},
    "today": {"year": 1990, "month": 1, "day": 1, "time": "00:00"},
}

def get_date():
    state = inky_helper.load_state(default_state)
    return state["date"]

def get_today():
    state = inky_helper.load_state(default_state)
    return state["today"]

def prev_page():
    print("PREVIOUS")
    state = inky_helper.load_state(default_state)
    print(state)
    if state["view"] == "month":
        if state["date"]["month"] == 1:
            state["date"]["year"] -= 1
            state["date"]["month"] = 12
        else:
            state["date"]["month"] -= 1
        inky_helper.save_state(state)
        month.update(display, state["date"], state["today"])
    elif state["view"] == "agenda":
        state["date"]["day"] -= 1
        inky_helper.save_state(state)
        agenda.draw_agenda(display, state["date"], state["today"])

def next_page():
    print("NEXT")
    state = inky_helper.load_state(default_state)
    print(state)
    if state["view"] == "month":
        if state["date"]["month"] == 12:
            state["date"]["year"] += 1
            state["date"]["month"] = 1
        else:
            state["date"]["month"] += 1
        inky_helper.save_state(state)
        month.update(display, state["date"], state["today"])
    elif state["view"] == "agenda":
        state["date"]["day"] += 1
        inky_helper.save_state(state)
        agenda.draw_agenda(display, state["date"], state["today"])

def today():
    # reset to today's page for whatever view
    print("TODAY")
    state = inky_helper.load_state(default_state)
    print(state)
    state["date"] = inky_helper.today()
    state["today"] = inky_helper.today()
    inky_helper.save_state(state)
    if state["view"] == "month":
        month.update(display, state["date"], state["today"])
    elif state["view"] == "agenda":
        agenda.draw_agenda(display, state["date"], state["today"])

def view_month():
    print("MONTH")
    state = inky_helper.load_state(default_state)
    print(state)
    state["view"] = "month"
    inky_helper.save_state(state)
    month.update(display, state["date"], state["today"])

def view_agenda():
    print("AGENDA")
    state = inky_helper.load_state(default_state)
    print(state)
    state["view"] = "agenda"
    inky_helper.save_state(state)
    agenda.draw_agenda(display, state["date"], state["today"])

def view_week():
    # TODO: TBC
    pass

def wake():
    pass

def sleep():
    pass
