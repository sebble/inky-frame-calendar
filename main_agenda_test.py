SLEEP_MINUTES=1

from secrets import WIFI_PASSWORD, WIFI_SSID
import time, machine, ical, inky_helper

print("main.py")

time.sleep(0.5)

print("awake")

connected = inky_helper.network_connect(WIFI_SSID, WIFI_PASSWORD)
if connected:
    print("connected")
    agenda = ical.get_agenda()
    print("updated")
    if len(agenda) > 0:
        print("Got %d items" % len(agenda))
    else:
        print("No items found")

print("Sleep for %d minutes ..." % SLEEP_MINUTES)
inky_helper.sleep(SLEEP_MINUTES)

print("awake")

machine.reset()

print("reset")
