
from secrets import WIFI_PASSWORD, WIFI_SSID
import network
import time

def init():
    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
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
