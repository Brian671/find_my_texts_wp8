"""
I was made aware of the Thread/Conversation structure by Physical Analyzer.

The Thread is stored in the following structure:

    \x04\x00\x01\x00
    (?P<id_short>(?P<id_byte>.))
    \x0C\x7F\x38\x00
    (?P<thread_id>....)
    .{4}
    \*{4}
    (?P<thread_length>.{4})
    (?P<u0>.{20})
    (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)
    (?P<message_count>.{4})
    (?P<u1>.{,160}?)
    (?:\x01(?P<phone_0>(?:..){,160}?))?
    \x01\x30\x00\xE1\xE0
    (?P<phone_1>(?:..){,160}?)\x00\x00\x01
    (?P<phone_2>(?:..){,160}?)\x00\x00\x00*?\x01
    (?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)

where id's of the form `u#` indicate regions with unknown meaning.



"""
from phone_analysis.recovery_expressions.thread_record import default, expressions
from phone_analysis.tools.utils import *
from phone_analysis.database import sms_database

__version__ = '9-12-2015'
__author__ = 'Chris Ottersen'

''' :type : int'''
THREAD_OFFSET_BEFORE = 250

''' :type : int'''
THREAD_OFFSET_AFTER = 200

''' :type : dict[str, object|None]'''
OUTPUT_TEMPLATE = {

    "record_offset": None,
    "thread_id": None,
    "thread_length": None,
    "u0": None,
    "FILETIME_0": None,
    "u1": None,
    "phone_0": None,
    "phone_1": None,
    "phone_2": None,
    "FILETIME_1": None,
    "full_binary": None
}


def parse_thread(fb, hit):
    """


    :param fb: open file in mode 'rb' -
    :type fb: file
    :param hit: unsigned long - indicating the offset from the beginning of fb to the thread marker
    :type hit: long
    :return: dict containing the parsed thread values
    :rtype: dict[str, object|None]
    """
    global THREAD_OFFSET_BEFORE
    global THREAD_OFFSET_AFTER

    ''' :type : dict[str,str|buffer|long|int|None] '''
    parsed = {}

    ''' :type : dict[str,dict[str,str|buffer|long|int|None]] '''
    output = {
        "conversation_type0_offsets": OUTPUT_TEMPLATE.copy(),
        "conversation_type0_widths": OUTPUT_TEMPLATE.copy(),
        "conversation_type0_stage0": OUTPUT_TEMPLATE.copy(),
        "conversation_type0_stage1": OUTPUT_TEMPLATE.copy()
    }

    fb.seek(hit - THREAD_OFFSET_BEFORE)

    ''':type : bool'''
    had_match = read_start(fb, output, parsed, THREAD_OFFSET_BEFORE)
    had_match = read_end(fb, had_match, output, parsed, THREAD_OFFSET_AFTER)

    if had_match:
        for key in OUTPUT_TEMPLATE.keys():
            if key not in parsed.keys():
                parsed[key] = None

        if "FILETIME_0" in parsed.keys() and isinstance(parsed["FILETIME_0"], str) and len(parsed["FILETIME_0"]) == 8:
            output["conversation_type0_stage1"]["FILETIME_0"] = struct.unpack("<Q", parsed["FILETIME_0"])[0]
        else:
            output["conversation_type0_stage1"]["FILETIME_0"] = None
        if "FILETIME_1" in parsed.keys() and isinstance(parsed["FILETIME_1"], str) and len(parsed["FILETIME_1"]) == 8:
            output["conversation_type0_stage1"]["FILETIME_1"] = struct.unpack("<Q", parsed["FILETIME_1"])[0]
        else:
            output["conversation_type0_stage1"]["FILETIME_1"] = None

        if parsed["thread_id"] is not None:
            parsed["thread_id"] = struct.unpack("<i", parsed["thread_id"])[0]
        output["conversation_type0_stage1"]["thread_id"] = parsed["thread_id"]

        if parsed["thread_length"] is not None:
            parsed["thread_length"] = struct.unpack("<i", parsed["thread_length"])[0]
        output["conversation_type0_stage1"]["thread_length"] = parsed["thread_length"]

        if isinstance(parsed["u1"], str):
            output["conversation_type0_stage1"]["u1"] = buffer(parsed["u1"])
        if isinstance(parsed["u0"], str):
            output["conversation_type0_stage1"]["u0"] = buffer(parsed["u0"])

        process_phones(parsed, output)
    else:
        parsed = None

    output["conversation_type0_offsets"]["record_offset"] = hit
    output["conversation_type0_stage0"]["record_offset"] = hit
    output["conversation_type0_stage1"]["record_offset"] = hit
    output["conversation_type0_widths"]["record_offset"] = hit
    insert(output)
    return parsed


def read_start(fb, output, parsed, offset=250):
    """

    :param fb: open file in mode 'rb'
    :type fb: file
    :param output:
    :type output: dict[str, dict[str,str|buffer|long|int|None]]
    :param parsed:
    :type parsed:dict[str,str|buffer|long|int|None]
    :param offset: unsigned long
    :type offset: long
    :return:
    :rtype: bool
    """
    start_chunk = fb.read(offset)
    start_match = expressions.start.exp.search(start_chunk)
    had_match = start_match is not None and start_match.groupdict() is not None

    if had_match:
        start_dict = start_match.groupdict().copy()
        parsed.update(start_dict)
        for key in start_dict.keys():
            if key in OUTPUT_TEMPLATE.keys() and start_dict[key] is not None:
                if key in expressions.start.exp.groupindex:
                    gindex = expressions.start.exp.groupindex[key]
                    output["conversation_type0_offsets"][key] = offset - start_match.start(gindex)
                    output["conversation_type0_widths"][key] = len(start_dict[key])
                    output["conversation_type0_stage0"][key] = buffer(start_dict[key])
                else:
                    output["conversation_type0_offsets"][key] = None
                    output["conversation_type0_widths"][key] = None
                    output["conversation_type0_stage0"][key] = None

        start_chunk = start_match.group(0)

    else:
        parsed.update(default.start.values.copy())

    output["conversation_type0_offsets"]["full_binary"] = start_chunk
    output["conversation_type0_widths"]["full_binary"] = start_chunk
    output["conversation_type0_stage0"]["full_binary"] = start_chunk
    output["conversation_type0_stage1"]["full_binary"] = start_chunk
    return had_match


def read_end(fb, had_match, output, parsed, offset=200):
    """

    :param fb: open file in mode 'rb'
    :type fb: file
    :param had_match:
    :type had_match: bool
    :param output:
    :type output: dict[str, dict[str,str|buffer|long|int|None]]
    :param parsed:
    :type parsed:dict[str,str|buffer|long|int|None]
    :param offset: unsigned long
    :type offset: long
    :return:
    :rtype: bool
    """
    end_chunk = fb.read(offset)
    end_match = expressions.end.exp.search(end_chunk)
    if end_match is not None and end_match.groupdict() is not None:
        end_dict = end_match.groupdict().copy()
        parsed.update(end_dict)
        for key in end_dict.keys():
            if key in OUTPUT_TEMPLATE.keys() and end_dict[key] is not None:
                if key in expressions.end.exp.groupindex:
                    gindex = expressions.end.exp.groupindex[key]
                    offset = end_match.start(gindex)
                    output["conversation_type0_offsets"][key] = offset
                    output["conversation_type0_widths"][key] = len(end_dict[key])
                    output["conversation_type0_stage0"][key] = buffer(end_dict[key])
                else:
                    output["conversation_type0_offsets"][key] = None
                    output["conversation_type0_widths"][key] = None
                    output["conversation_type0_stage0"][key] = None

        end_chunk = end_match.group(0)

        had_match = True
    else:
        parsed.update(default.end.values.copy())

    end_chunk = buffer(output["conversation_type0_offsets"]["full_binary"] + end_chunk)
    output["conversation_type0_offsets"]["full_binary"] = end_chunk
    output["conversation_type0_widths"]["full_binary"] = end_chunk
    output["conversation_type0_stage0"]["full_binary"] = end_chunk
    output["conversation_type0_stage1"]["full_binary"] = end_chunk

    return had_match


def process_phones(parsed, output):
    """

    :param parsed:
    :type parsed:dict[str,str|buffer|long|int|None]
    :param output:
    :type output: dict[str, dict[str,str|buffer|long|int|None]]
    :return:
    :rtype: None
    """

    phones = []
    parsed["Phones"] = phones
    for phone in range(0, 3):
        key = "phone_%d" % phone
        if key in parsed:
            if isinstance(parsed[key], str):
                p = parsed[key]
                assert isinstance(p, str)
                parsed[key] = p.decode('utf-16le')
                output["conversation_type0_stage1"][key] = parsed[key]
                phones.append(parsed[key])
        else:
            output["conversation_type0_stage1"][key] = None
            parsed[key] = None


def insert(output):
    """

    :param output:
    :type output: dict[str, dict[object]]
    :return: no return value
    :rtype: None
    """
    global OUTPUT_TEMPLATE

    cursor = sms_database.cursor
    db = sms_database.db
    keys = OUTPUT_TEMPLATE.keys()

    query = """
              INSERT INTO %%s(%s)
              VALUES (:%s);
            """ % (", ".join(keys), ", :".join(keys))
    for conversation_type0 in output.keys():
        q = query % conversation_type0
        cursor.execute(q, output[conversation_type0])

    db.commit()
