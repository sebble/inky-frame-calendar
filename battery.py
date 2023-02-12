# This example reads Inky Frame's system voltage
# and estimates how much charge is left in the battery
# Save this code as main.py if you want it to run automatically!

from machine import ADC, Pin
import time

from picographics import PicoGraphics, DISPLAY_INKY_FRAME

# these are our reference voltages for a full/empty battery, in volts
# the values could vary by battery size/manufacturer so you might need to adjust them
# e.g. for 2xAA or AAA batteries, try max 3.4 min 3.0
full_battery = 4.2
empty_battery = 2.8

# colours to draw with
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7

# set up the display
display = PicoGraphics(display=DISPLAY_INKY_FRAME)

# and the activity LED
activity_led = Pin(6, Pin.OUT)
activity_led.on()

# set up and enable vsys hold so Inky Frame doesn't go to sleep
HOLD_VSYS_EN_PIN = 2

hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)
hold_vsys_en_pin.value(True)

# set up the ADC that's connected to the system input voltage
vsys = ADC(29)

# on a Pico W we need to pull GP25 high to be able to read vsys
# this is because this pin is shared with the wireless module's SPI interface
spi_output = (Pin(25, Pin.OUT))
spi_output.value(True)

# how we convert the reading into a voltage
conversion_factor = 3 * 3.3 / 65535
     
# convert the raw ADC read into a voltage, and then a percentage
voltage = vsys.read_u16() * conversion_factor
percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
if percentage > 100:
    percentage = 100.00

# monitoring vbus tells us if Inky is being USB powered
# it seems to not always identify USB power correctly when run through Thonny?
vbus = Pin('WL_GPIO2', Pin.IN)

# draw the battery outline
display.set_pen(WHITE)
display.clear()
display.set_pen(BLACK)
display.rectangle(0, 0, 220, 135)
display.rectangle(220, 40, 20, 55)
display.set_pen(WHITE)
display.rectangle(3, 3, 214, 129)

# draw a box for the battery level
display.set_pen(YELLOW)
display.rectangle(5, 5, round(210 / 100 * percentage), 125)

# add text
if vbus.value():
    display.set_pen(BLUE)
    display.text('USB power!', 15, 10, 240, 3)
else:
    display.set_pen(RED)
    display.text('{:.2f}'.format(voltage) + "v", 15, 10, 240, 5)
    display.text('{:.0f}%'.format(percentage), 15, 50, 240, 5)

display.update()

# go to sleep until someone pushes a button
# (this will only work if code is saved as main.py and on battery power)
activity_led.off()
hold_vsys_en_pin.init(Pin.IN)