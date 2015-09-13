__author__ = 'owner'

from phone_analysis.recovery_expressions.thread_record import default, expressions
from phone_analysis.tools.utils import *

values = {
    "id": None,
    "id_byte": None,
    "id_long": None,
    "thread_length": None,
    "u0": None,
    "FILETIME_0": None,
    "count_byte": None,
    "u1": None,
    "phone_0": None,
    "phone_1": None,
    "phone_2": None,
    "FILETIME_1": None
}


def parse_thread(fb, hit):
    start_match = None
    end_match = None        # match
    had_match = False
    parsed = {}
    fb.seek(hit-800)

    start_match = expressions.start.exp.search(fb.read(800))
    if start_match is not None and start_match.groupdict() is not None:
        parsed.update(start_match.groupdict().copy())
        had_match = True
    else:
        parsed.update(default.start.values.copy())

    end_match = expressions.end.exp.search(fb.read(800))
    if end_match is not None and end_match.groupdict() is not None:
        parsed.update(end_match.groupdict().copy())
        had_match = True
    else:
        parsed.update(default.end.values.copy().copy())

    if had_match:
        (parsed["FILETIME_0"], f0) = to_datetime(parsed["FILETIME_0"])
        (parsed["FILETIME_1"], f1) = to_datetime(parsed["FILETIME_1"])

        if parsed["FILETIME_1"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_1"].strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)")
            parsed["timestamp"] = f1
        elif parsed["FILETIME_0"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_0"].strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)")
            parsed["timestamp"] = f1
        else:
            parsed["Formatted Date"] = None
            parsed["timestamp"] = None
        if parsed["thread_id"] is None:
            parsed["thread_id"] = "\xFF\xFF\xFF\xFF"

        parsed["thread_id"] = struct.unpack(">i", parsed["thread_id"])[0]
        parsed["u0"] = to_hex(parsed["u0"])
        parsed["u1"] = to_hex(parsed["u1"])
        parsed["thread_length"] = struct.unpack(">i", parsed["thread_length"])[0]
        parsed["phone_0"] = to_unicode(parsed["phone_0"])
        parsed["phone_1"] = to_unicode(parsed["phone_1"])
        parsed["phone_2"] = to_unicode(parsed["phone_2"])
        parsed["phone_3"] = to_unicode(parsed["phone_2"])

        parsed["All Dates"] = [parsed["FILETIME_0"], parsed["FILETIME_1"]]
        parsed["Formatted Date"] = parsed["Formatted Date"]
        parsed["ID"] = parsed["thread_id"]
        parsed["Thread Length"] = parsed["thread_length"]
        parsed["Phones"] = [parsed["phone_0"], parsed["phone_1"], parsed["phone_2"], parsed["phone_2"]]

        return parsed
    else:
        return None
