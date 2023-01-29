def read_until(stream, char):
    result = b""
    while True:
        c = stream.read(1)
        if c == char:
            return result
        result += c


def discard_until(stream, c):
    while stream.read(1) != c:
        pass

def parse_ical_feed(s, start_date = (2023,01,01), max_items = 10):
    events = []
    while True:
        char = s.read(1)
        if len(char) == 0:
            break
        
        discard_until(s, b"\n")
        field = read_until(s, b":")
        value = read_until(s, b"\n")
        
        print([field, value])
        gc.collect()


# import ssl
# scontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

def get_ical(url):
    print("get")
    try:
        print("try")
        stream = urequest.urlopen(url, context=scontext)
        print("stream")
        output = list(parse_ical_feed(stream))
        print("output")
        return output

    except OSError as e:
        print(e)
        return False