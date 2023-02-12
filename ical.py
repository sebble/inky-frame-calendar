from urllib import urequest
import gc
import ujson
from secrets import FUNCTION_URL

def get_agenda():
    print("get_agenda")
    gc.collect()
    try:
        socket = urequest.urlopen(FUNCTION_URL)
        print("socket")
        j = ujson.load(socket)
        print("json")
        socket.close()
        print(j)
        gc.collect()
        print("cleaned")
        return j
    except OSError:
        print("ERROR LOADING ICAL")
    return []