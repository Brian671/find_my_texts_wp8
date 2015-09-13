__author__ = 'owner'

from phone_analysis.tools.utils import *
from phone_analysis.recovery_expressions.sms_text import expressions

DIRECTIONS = {
    "\x00\x00\x00\x00": "unread",
    "\x01\x00\x00\x00": "read",
    "\x21\x00\x00\x00": "sent",
    "\x29\x00\x00\x00": "draft"
}


def get_direction(s):
    if s in DIRECTIONS.keys():
        s = DIRECTIONS[s]
    return s


def parse_sms(fb, hit):
    message_start_match = None
    message_end_match = None        # match
    had_match = False
    parsed = {}
    fb.seek(hit-800)

    message_start_match = expressions.start.exp.search(fb.read(800))
    if message_start_match is not None and message_start_match.groupdict() is not None:
        parsed.update(message_start_match.groupdict().copy())
        if parsed["direction"] == "\x00\x00\x00\x00" or parsed["direction"] == "\x01\x00\x00\x00":
            end_exp = expressions.end.exp_incoming
        elif parsed["direction"] == "\x20\x00\x00\x00" or parsed["direction"] == "\x29\x00\x00\x00":
            end_exp = expressions.end.exp_outgoing
        else:
            end_exp = expressions.end.exp_general
        had_match = True
    else:
        parsed.update(phone_analysis.recovery_expressions.sms_text.default.type0.start.values.copy())
        end_exp = expressions.end.exp_general

    message_end_match = end_exp.search(fb.read(1500))
    if message_end_match is not None and message_end_match.groupdict() is not None:
        parsed.update(message_end_match.groupdict().copy())
        had_match = True
    else:
        parsed.update(phone_analysis.recovery_expressions.sms_text.default.type0.end.values.copy().copy())

    if had_match:

        parsed["direction"] = get_direction(parsed["direction"])
        (parsed["FILETIME_0"], f0) = to_datetime(parsed["FILETIME_0"])
        (parsed["FILETIME_1"], f1) = to_datetime(parsed["FILETIME_1"])
        (parsed["FILETIME_2"], f2) = to_datetime(parsed["FILETIME_2"])
        (parsed["FILETIME_3"], f3) = to_datetime(parsed["FILETIME_3"])

        if parsed["FILETIME_3"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_3"]
            parsed["record_id"] = parsed["FILETIME_3"]
            parsed["timestamp"] = f0
        elif parsed["FILETIME_2"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_2"]
            parsed["record_id"] = parsed["FILETIME_2"]
            parsed["timestamp"] = f1
        elif parsed["FILETIME_1"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_1"]
            parsed["record_id"] = parsed["FILETIME_1"]
            parsed["timestamp"] = f2
        elif parsed["FILETIME_0"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_0"]
            parsed["record_id"] = parsed["FILETIME_0"]
            parsed["timestamp"] = f3
        else:
            parsed["Formatted Date"] = None
            parsed["record_id"] = None
            parsed["timestamp"] = None

        if parsed["Formatted Date"] is not None:
            parsed["Formatted Date"] = parsed["Formatted Date"].strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)")

        if parsed["direction"] == "read" or parsed["direction"] == "unread":
            parsed["phone_0"] = to_unicode(parsed["phone_0"])
            parsed["phone_1"] = to_unicode(parsed["phone_1"])
            parsed["phone_2"] = to_unicode(parsed["phone_2"])
            parsed["phone_3"] = to_unicode(parsed["phone_3"])
            parsed["Phones"] = [parsed["phone_0"], parsed["phone_1"], parsed["phone_2"], parsed["phone_3"]]
            parsed["u11"] = parsed["u11a"]
        else:
            parsed["phone_0"] = None
            parsed["phone_1"] = None
            parsed["phone_2"] = None
            parsed["phone_3"] = None
            parsed["Phones"] = None

        parsed["message"] = to_unicode(parsed["message"])
        parsed["sim"] = to_unicode(parsed["sim"])
        parsed["SMStext"] = to_unicode(parsed["SMStext"])

        if parsed["thread_id"] is None:
            parsed["thread_id"] = "\xFF\xFF\xFF\xFF"

        parsed["thread_id"] = struct.unpack("<i", parsed["thread_id"])[0]

        if parsed["message_id"] is not None:
            parsed["message_id"] = struct.unpack("<i", parsed["message_id"])[0]

        parsed["u0"] = to_hex(parsed["u0"])
        parsed["u1"] = to_hex(parsed["u1"])
        parsed["u2"] = to_hex(parsed["u2"])
        parsed["u3"] = to_hex(parsed["u3"])
        parsed["u4"] = to_hex(parsed["u4"])
        parsed["u5"] = to_hex(parsed["u5"])
        parsed["u6"] = to_hex(parsed["u6"])
        parsed["u7"] = to_hex(parsed["u7"])
        parsed["u8"] = to_hex(parsed["u8"])
        parsed["u9"] = to_hex(parsed["u9"])
        parsed["u10"] = to_hex(parsed["u10"])
        parsed["u12"] = to_hex(parsed["u12"])
        parsed["hit"] = hit

        parsed.__delitem__("content")
        parsed.__delitem__("u11a")
    else:
        parsed = None
        print ("miss: %d - %x" % (hit, hit))
    return parsed
