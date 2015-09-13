"""
This script

#. version
"""

from phone_analysis.tools.utils import *
from phone_analysis.recovery_expressions.sms_text import expressions
from phone_analysis.recovery_expressions.sms_text import default
from phone_analysis.database import sms_database

__author__ = 'Chris Ottersen'
__version__ = '9-12-2015'
type_0_count = 0
type_1_count = 0

''' :type : dict[str, object|None] '''
OUTPUT_TEMPLATE = {
    "record_offset": None,
    "u0": None,
    "message_id": None,
    "u1": None,
    "thread_id": None,
    "u2": None,
    "FILETIME_0": None,
    "FILETIME_1": None,
    "direction": None,
    "FILETIME_2": None,
    "u3": None,
    "u4": None,
    "u5": None,
    "u6": None,
    "u7": None,
    "u8": None,
    "u9": None,
    "u10": None,
    "u11": None,
    "u11a": None,
    "phone_0": None,
    "SMStext": None,
    "content": None,
    "phone_1": None,
    "phone_2": None,
    "phone_3": None,
    "message": None,
    "FILETIME_2b": None,
    "u12": None,
    "FILETIME_3": None,
    "sim": None,
    "full_binary": None
}

''' :type : dict[str, str|None] '''
DIRECTIONS = {
    "\x00\x00\x00\x00": "unread",
    "\x01\x00\x00\x00": "read",
    "\x21\x00\x00\x00": "sent",
    "\x29\x00\x00\x00": "draft"
}


def get_direction(s):
    """

    :param s:
    :type s: str
    :return:
    :rtype: str
    """
    if s in DIRECTIONS.keys():
        s = DIRECTIONS[s]
    return s


def parse_sms(fb, hit):
    """


    :param fb: open file in mode 'rb' -
    :type fb: file
    :param hit: unsigned long - indicating the offset from the beginning of fb to the sms marker
    :type hit: long
    :return: dict<str, object> - dict containing the parsed sms values
    :rtype: dict[str, object]
    """
    global type_0_count
    global type_1_count
    global OUTPUT_TEMPLATE
    start_offset = 5000
    end_offset = 5000
    had_match = False
    parsed = {}
    fb.seek(hit-start_offset)

    output = {
        "sms_type0_offsets": OUTPUT_TEMPLATE.copy(),
        "sms_type0_widths": OUTPUT_TEMPLATE.copy(),
        "sms_type0_stage0": OUTPUT_TEMPLATE.copy(),
        "sms_type0_stage1": OUTPUT_TEMPLATE.copy()
    }
    output["sms_type0_offsets"]["hit"] = hit
    output["sms_type0_stage0"]["hit"] = hit
    output["sms_type0_stage1"]["hit"] = hit
    output["sms_type0_widths"]["hit"] = hit

    output["sms_type0_offsets"]["record_offset"] = hit
    output["sms_type0_stage0"]["record_offset"] = hit
    output["sms_type0_stage1"]["record_offset"] = hit
    output["sms_type0_widths"]["record_offset"] = hit

    (end_exp, had_match) = read_start(fb, had_match, output, parsed, start_offset)

    had_match = read_end(end_exp, fb, had_match, output, parsed, end_offset)

    if had_match:

        parsed["direction"] = get_direction(parsed["direction"])
        output["sms_type0_stage1"]["direction"] = parsed["direction"]
        process_phones(parsed, output)

        if parsed["message"] is not None:
            output["sms_type0_stage1"]["message"] = parsed["message"][::2]
        parsed["message"] = to_unicode(parsed["message"])

        output["sms_type0_stage1"]["sim"] = parsed["sim"] is not None
        parsed["sim"] = to_unicode(parsed["sim"])

        if parsed["SMStext"] is not None:
            output["sms_type0_stage1"]["SMStext"] = parsed["SMStext"][::2]
        parsed["SMStext"] = to_unicode(parsed["SMStext"])

        if parsed["thread_id"] is None:
            parsed["thread_id"] = None
        else:
            parsed["thread_id"] = struct.unpack("<i", parsed["thread_id"])[0]
        output["sms_type0_stage1"]["thread_id"] = parsed["thread_id"]

        if parsed["message_id"] is None:
            parsed["message_id"] = None
        else:
            parsed["message_id"] = struct.unpack("<i", parsed["message_id"])[0]
        output["sms_type0_stage1"]["message_id"] = parsed["message_id"]

        parsed["hit"] = hit
        output["sms_type0_stage1"]["hit"] = hit
        if isinstance(parsed["FILETIME_0"], str) and len(parsed["FILETIME_0"]) == 8:
            output["sms_type0_stage1"]["FILETIME_0"] = struct.unpack("<Q", parsed["FILETIME_0"])[0]
        if isinstance(parsed["FILETIME_1"], str) and len(parsed["FILETIME_1"]) == 8:
            output["sms_type0_stage1"]["FILETIME_1"] = struct.unpack("<Q", parsed["FILETIME_1"])[0]
        if isinstance(parsed["FILETIME_2"], str) and len(parsed["FILETIME_2"]) == 8:
            output["sms_type0_stage1"]["FILETIME_2"] = struct.unpack("<Q", parsed["FILETIME_2"])[0]
        if isinstance(parsed["FILETIME_2b"], str) and len(parsed["FILETIME_2b"]) == 8:
            output["sms_type0_stage1"]["FILETIME_2b"] = struct.unpack("<Q", parsed["FILETIME_2b"])[0]
        if isinstance(parsed["FILETIME_3"], str) and len(parsed["FILETIME_3"]) == 8:
            output["sms_type0_stage1"]["FILETIME_3"] = struct.unpack("<Q", parsed["FILETIME_3"])[0]

        (f0, parsed["FILETIME_0"]) = to_datetime(parsed["FILETIME_0"])
        (f1, parsed["FILETIME_1"]) = to_datetime(parsed["FILETIME_1"])
        (f2, parsed["FILETIME_2"]) = to_datetime(parsed["FILETIME_2"])
        (f3, parsed["FILETIME_3"]) = to_datetime(parsed["FILETIME_3"])

        process_unknowns(parsed, output)
        temp = parsed["FILETIME_0"]
        parsed["FILETIME_0"] = f0
        f0 = temp
        temp = parsed["FILETIME_1"]
        parsed["FILETIME_1"] = f1
        f1 = temp
        temp = parsed["FILETIME_2"]
        parsed["FILETIME_2"] = f2
        f2 = temp
        temp = parsed["FILETIME_3"]
        parsed["FILETIME_3"] = f3
        f3 = temp

        if parsed["FILETIME_3"] is not None:
            parsed["Formatted Date"] = parsed["FILETIME_3"]
            parsed["record_id"] = parsed["FILETIME_3"]
            parsed["timestamp"] = f0
        elif parsed["FILETIME_2"] is not None:
            parsed["version"] = "8.1.x"
            parsed["Formatted Date"] = parsed["FILETIME_2"]
            parsed["record_id"] = parsed["FILETIME_2"]
            parsed["timestamp"] = f1
        elif "FILETIME_2b" in parsed.keys() and parsed["FILETIME_2b"] is not None:
            parsed["FILETIME_2"] = parsed["FILETIME_2b"]
            parsed["version"] = "8.0.x"
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
        type_0_count += 1
        print("type 0: %d" % type_0_count)
    else:
        parsed = None
        message_start_match_t1 = expressions.type1.full.exp.search(output["sms_type0_stage1"]["full_binary"])
        if message_start_match_t1 is not None and message_start_match_t1.groupdict() is not None:
            d = message_start_match_t1.groupdict()
            type_1_count += 1
            print("type 1: %d" % type_1_count)
        else:
            print("miss: %d - %x" % (hit, hit))
    insert(output)

    return parsed


def insert(output):
    """

    :param output:
    :type output: dict[str, dict[str, object]]
    :return:
    :rtype: int
    """
    global OUTPUT_TEMPLATE
    cursor = sms_database.cursor
    db = sms_database.db
    keys = OUTPUT_TEMPLATE.keys()

    query = """
              INSERT INTO %%s(%s)
              VALUES (:%s);
            """ % (", ".join(keys), ", :".join(keys))
    for sms_type0 in output.keys():
        try:
            q = query % sms_type0
            cursor.execute(q, output[sms_type0])
        except ValueError as e:
            db.rollback()
            print("%r at %r" % (output[sms_type0]["record_offset"], e))
            return -1

    db.commit()
    return 0


def process_unknowns(parsed, output):
    """

    :param parsed:
    :type parsed: dict[str, object]
    :param output:
    :type output: dict[str, dict[str, object]]
    :return:
    :rtype: None
    """
    for u in range(0, 13):
        key = "u%d" % u
        if parsed[key] is not None:
            output["sms_type0_stage1"][key] = buffer(parsed[key])
            parsed[key] = to_hex(parsed[key])
    if parsed["u11a"] is not None:
        output["sms_type0_stage1"]["u11a"] = buffer(parsed["u11a"])
        parsed["u11a"] = to_hex(parsed["u11a"])


def process_phones(parsed, output):
    """

    :param parsed:
    :type parsed: dict[str, object]
    :param output:
    :type output: dict[str, dict[str, object]]
    :return: the number of distinct party id's for this call
    :rtype: int
    """
    Phones = []
    if parsed["direction"] == "read" or parsed["direction"] == "unread":

        parsed["Phones"] = Phones

        for phone in range(0, 4):
            key = "phone_%d" % phone
            if isinstance(parsed[key], str):
                output["sms_type0_stage1"][key] = parsed[key][::2]
                parsed[key] = to_unicode(parsed[key])
            Phones.append(parsed[key])

        parsed["u11"] = parsed["u11a"]
    else:
        parsed["phone_0"] = None
        output["sms_type0_stage1"]["phone_0"] = None
        parsed["phone_1"] = None
        output["sms_type0_stage1"]["phone_1"] = None
        parsed["phone_2"] = None
        output["sms_type0_stage1"]["phone_2"] = None
        parsed["phone_3"] = None
        output["sms_type0_stage1"]["phone_3"] = None
        parsed["Phones"] = None

    return len(Phones)


def read_start(fb, had_match, output, parsed, offset=800):
    """

    :param fb:
    :type fb: file
    :param had_match:
    :type had_match: bool
    :param output:
    :type output: dict[str, dict[str, object]]
    :param parsed:
    :type parsed: dict[str, object]
    :return:
    :rtype: (re, bool)
    """
    global OUTPUT_TEMPLATE
    start_chunk = fb.read(offset)
    message_start_match = expressions.type0.start.exp.search(start_chunk)
    if message_start_match is not None and message_start_match.groupdict() is not None:
        start_dict = message_start_match.groupdict().copy()
        parsed.update(start_dict)

        for key in start_dict.keys():
            if key in OUTPUT_TEMPLATE.keys() and start_dict[key] is not None:
                gindex = expressions.type0.start.exp.groupindex[key]
                offset -= message_start_match.start(gindex)
                output["sms_type0_offsets"][key] = offset
                output["sms_type0_widths"][key] = len(start_dict[key])
                output["sms_type0_stage0"][key] = buffer(start_dict[key])

        start_chunk = message_start_match.group(0)

        if parsed["direction"] == "\x00\x00\x00\x00" or parsed["direction"] == "\x01\x00\x00\x00":
            end_exp = expressions.type0.end.exp_incoming
        elif parsed["direction"] == "\x21\x00\x00\x00" or parsed["direction"] == "\x29\x00\x00\x00":
            end_exp = expressions.type0.end.exp_outgoing
        else:
            end_exp = expressions.type0.end.exp_general
        had_match = True
    else:
        parsed.update(default.type0.start.values.copy())
        end_exp = expressions.type0.end.exp_general
    output["sms_type0_offsets"]["full_binary"] = start_chunk
    output["sms_type0_widths"]["full_binary"] = start_chunk
    output["sms_type0_stage0"]["full_binary"] = start_chunk
    output["sms_type0_stage1"]["full_binary"] = start_chunk
    return (end_exp, had_match)


def read_end(end_exp, fb, had_match, output, parsed, offset=5000):
    """

    :param end_exp:
    :type end_exp: re
    :param fb:
    :type fb: file
    :param had_match:
    :type had_match: bool
    :param output:
    :type output: dict[str, dict[str, object]]
    :param parsed:
    :type parsed: dict[str, object]
    :param offset:
    :type offset: int
    :return:
    :rtype: bool
    """
    global OUTPUT_TEMPLATE
    end_chunk = fb.read(offset)
    message_end_match = end_exp.search(end_chunk)
    if message_end_match is not None and message_end_match.groupdict() is not None:
        end_dict = message_end_match.groupdict().copy()

        parsed.update(end_dict)

        for key in end_dict.keys():
            if key in OUTPUT_TEMPLATE.keys() and end_dict[key] is not None:
                gindex = end_exp.groupindex[key]
                offset = message_end_match.start(gindex)
                output["sms_type0_offsets"][key] = offset
                output["sms_type0_widths"][key] = len(end_dict[key])
                output["sms_type0_stage0"][key] = buffer(end_dict[key])
        end_chunk = message_end_match.group(0)
        had_match = True
    else:

        parsed.update(default.type0.end.values.copy())
    full = buffer(output["sms_type0_offsets"]["full_binary"] + end_chunk)

    output["sms_type0_offsets"]["full_binary"] = full
    output["sms_type0_widths"]["full_binary"] = full
    output["sms_type0_stage0"]["full_binary"] = full
    output["sms_type0_stage1"]["full_binary"] = full
    return had_match

