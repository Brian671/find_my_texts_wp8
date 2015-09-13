__author__ = 'owner'
import re
import struct
import datetime
import tz_utils

datetime_counter = 0


def to_unicode(s, base=2):
    if s is not None:
        s = re.compile("^((?:.{%d})+?)(?:\x00{%d}|$)" % (base, base), re.DOTALL).search(s)
        if s is not None:
            s = s.group(1)
            s = u"".join([unichr(ord(s[i * base]) + (ord(s[i * base + 1]) >> 8)) for i in range(0, len(s) // base)])
        else:
            s = "None"
    else:
        s = "None"
    return s


def to_hex(s):
    #http://stackoverflow.com/questions/12214801/print-a-string-as-hex-bytes
    if s is not None:
        s = " ".join("{:02X}".format(ord(c)) for c in s)
    else:
        s = "None"
    return s


def to_datetime(s):
    global datetime_counter
    if s is not None:
        f = struct.unpack('<Q', s)[0] - 116444736000000000
        temp = datetime.datetime.utcfromtimestamp(f // 10000000)
        out_datetime = datetime.datetime(
            int(temp.year),
            int(temp.month),
            int(temp.day),
            int(temp.hour),
            int(temp.minute),
            int(temp.second),
            int((f % 10000000) // 10),
            tz_utils.Local)
        out = (out_datetime, f * 1000 + datetime_counter)
    else:
        out = (None, datetime_counter)
    datetime_counter += 1
    return out
