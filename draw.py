BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

def title(msg, offset = 0):
    display.set_pen(BLACK)
    display.text(msg, offset, 0, 600, 4)

def outline(x, y, w, h, thickness = 3, colour = BLACK, fill = WHITE):
    display.set_pen(colour)
    display.rectangle(x - thickness, y - thickness, w + 2*thickness, h + 2*thickness)
    display.set_pen(fill)
    display.rectangle(x, y, w, h)

def nav(buttons):
    pos_x = 0
    pos_y = 422
    font_size = 3
    outline(250, 418, 100, 50)
    for i, (label, adjust) in enumerate(buttons):
        offset_x = int(i * 600 / 5) + pos_x + adjust
        display.set_pen(BLACK)
        display.text(label, offset_x, pos_y, int(600 / 5), font_size)
