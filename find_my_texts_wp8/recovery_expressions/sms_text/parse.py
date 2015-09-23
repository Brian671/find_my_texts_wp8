"""
This script

#. version
"""
import struct

import expressions

__author__ = 'Chris Ottersen'
__version__ = '9-12-2015'
miss = 0
type_0_count = 0
type_0_full_count = 0
type_0_partial_count = 0
type_1_full_count = 0
type_1_partial_count = 0
total_count = 0
hit_count = 0
DEFAULT_START_SIZE = 10000
DEFAULT_END_SIZE = 6000


"""
:type : dict[str, dict[str, object|None]]
"""
OUTPUT_TEMPLATES = {}

db = None
cursor = None
tables = None
def init_sms_text(db_param, tables_param):
    global tables
    global OUTPUT_TEMPLATES
    global db
    global cursor
    tables = tables_param
    db = db_param
    OUTPUT_TEMPLATES = {
        "sms_type0": {key: None for key in tables["sms_type0"].keys()},
        "sms_type1": {key: None for key in tables["sms_type1"].keys()}
    }
    cursor = db.cursor()



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
        return DIRECTIONS[s]
    else:
        return None


def unpack_unicode(x):
    """

    :param x:
    :type x: str
    :return:
    :rtype:
    """
    if x is not None and isinstance(x, str):
        return x.decode('utf-16le').encode('ascii', 'xmlcharrefreplace')


def unpack_date(x):
    """

    :param x:
    :type x:
    :return:
    :rtype:
    """
    if x is not None and isinstance(x, str) and len(x) == 8:
        return struct.unpack("<Q", x)[0]


def unpack_int(x):
    """

    :param x:
    :type x:
    :return:
    :rtype:
    """
    if x is not None and isinstance(x, str) and len(x) == 4:
        return struct.unpack("<i", x)[0]


def unpack_direction(x):
    """

    :param x:
    :type x:
    :return:
    :rtype:
    """
    if x is not None and isinstance(x, str) and len(x) == 4:
        d = struct.unpack("<i", x)[0]
        if d in DIRECTIONS.keys():
            return d
    return None


def unpack_message_id(parsed):
    """

    :param parsed:
    :type parsed: dict[str, str]|None
    :return:
    :rtype: int|None
    """
    message_id = None
    if parsed is None:
        pass

    elif "message_id" in parsed.keys() and parsed["message_id"] is not None:
        message_id = unpack_int(parsed["message_id"])

    elif "id_in" in parsed.keys() and parsed["id_in"] is not None:
        message_id = unpack_int(parsed["id_in"])

    elif "i0" in parsed.keys() and "i1" in parsed.keys() and \
            parsed["i0"] is not None and parsed["i1"] is not None:
        message_id = unpack_int(str(parsed["i0"]) + str(parsed["i1"]) + r"\x00\x00")

    elif "id0a" in parsed.keys() and "id1a" in parsed.keys() and \
            parsed["id0a"] is not None and parsed["id1a"] is not None:
        message_id = unpack_int(str(parsed["id0a"]) + str(parsed["id1a"]) + r"\x00\x00")

    return message_id


def unpack_thread_id(parsed):
    """

    :param parsed:
    :type parsed: dict[str, str]|None
    :return:
    :rtype: int|None
    """
    thread_id = None
    if parsed is None:
        pass

    elif "thread_id" in parsed.keys() and parsed["thread_id"] is not None:
        thread_id = unpack_int(parsed["thread_id"])

    #  elif "id_in" in parsed.keys() and parsed["id_in"] is not None:
    #      message_id = unpack_int(parsed["id_in"])

    elif "i0" in parsed.keys() and "i1" in parsed.keys() and \
            parsed["i0"] is not None and parsed["i1"] is not None:
        thread_id = unpack_int(str(parsed["i0"]) + str(parsed["i1"]) + r"\x00\x00")

    #  elif "id0a" in parsed.keys() and "id1a" in parsed.keys() and \
    #                  parsed["id0a"] is not None and parsed["id1a"] is not None:
    #      message_id = unpack_int(str(parsed["id0a"]) + str(parsed["id1a"]) + r"\x00\x00")

    return thread_id


def parse_sms(fb, hit):
    """


    :param fb: open file in mode 'rb' -
    :type fb: file
    :param hit: unsigned long - indicating the offset from the beginning of fb to the sms marker
    :type hit: long
    :return: dict<str, object> - dict containing the parsed sms values
    :rtype: dict[str, object]
    """
    global DEFAULT_START_SIZE
    global DEFAULT_END_SIZE
    global type_0_count
    global type_1_full_count
    global type_1_partial_count
    global miss
    global total_count
    global hit_count
    fb.seek(hit - DEFAULT_START_SIZE)
    full_buffer = fb.read(DEFAULT_END_SIZE + DEFAULT_START_SIZE)

    (type_0_start_match, type_0_end_match) = parse_sms_general(hit, "sms_type0", full_buffer)
    (type_1_start_match, type_1_end_match) = parse_sms_general(hit, "sms_type1", full_buffer,
                                                               pre_process=type1_pre_process)
    #  (type_2_start_match, type_2_end_match) = parse_sms_general(hit, "sms_type2", full_buffer)
    #  (type_3_start_match, type_3_end_match) = parse_sms_general(hit, "sms_type3", full_buffer)
    had_match = (type_0_start_match or type_0_start_match or
                 type_1_start_match or type_1_start_match)  # or
    #             type_2_start_match or type_2_start_match or
    #             type_3_start_match or type_3_start_match)
    if not had_match:
        miss += 1
        print("%02X -> miss: %d" % (hit, miss))


def get_start_expression(output_type):
    if output_type == "sms_type0":
        return expressions.type0.start.exp
    if output_type == "sms_type1":
        return expressions.type1.start.exp


def get_end_expression(parsed, output_type=None):
    global OUTPUT_TEMPLATES
    expression = None

    if (parsed is not None and not isinstance(parsed, dict)):
        raise Warning("for %r: parsed must be NoneType or dict. %r provided" % (output_type, type(parsed)))
    elif output_type == "sms_type0":

        if(parsed is None):
            expression = expressions.type0.end.exp_general

        elif("direction" not in parsed.keys() or parsed["direction"] is None):
            expression = expressions.type0.end.exp_general

        elif(isinstance(parsed["direction"], str)):
            if(len(parsed["direction"]) == 0):
                expression = expressions.type0.end.exp_general
            elif(parsed["direction"][0] == '\x21' or parsed["direction"][0] == '\x29'):
                expression = expressions.type0.end.exp_outgoing
            elif(parsed["direction"][0] == '\x01' or parsed["direction"][0] == '\x00'):
                expression = expressions.type0.end.exp_incoming
            else:
                expression = expressions.type0.end.exp_general

        elif(isinstance(parsed["direction"], int)):
            d = parsed["direction"] & 0xFF
            if (d == 0x21 or d == 0x29):
                expression = expressions.type0.end.exp_outgoing
            elif (d == 0x01 or d == 0x00):
                expression = expressions.type0.end.exp_incoming
            else:
                expression = expressions.type0.end.exp_general

    elif output_type == "sms_type1":
        if (parsed is None):
            expression = expressions.type1.end.get_end()
        else:
            if ('i0' not in parsed):
                parsed['i0'] = None
            if ('i1' not in parsed):
                parsed['i1'] = None
            if ('backwards' in parsed.keys()):
                expression = expressions.type1.end.get_end(parsed['phone_1'],
                                                           parsed['i0'],
                                                           parsed['i1'],
                                                           parsed['backwards'])
            else:
                expression = expressions.type1.end.get_end(parsed['phone_1'], parsed['i0'], parsed['i1'])

    return expression


def parse_sms_general(hit, output_type, full_binary, post_process=None, pre_process=None):
    global DEFAULT_END_SIZE
    global DEFAULT_START_SIZE
    global OUTPUT_TEMPLATES
    global tables
    assert full_binary is not None

    parsed = OUTPUT_TEMPLATES[output_type].copy()

    parsed["record_offset"] = hit
    output = {
        "offsets": parsed.copy(),
        "widths": parsed.copy(),
        "stage0": parsed.copy(),
        "stage1": parsed.copy()
    }
    start_expression = get_start_expression(output_type)
    start_match = start_expression.search(full_binary, 0, DEFAULT_START_SIZE)

    start_matched = start_match is not None
    if (start_matched):
        start_match_dict = start_match.groupdict()
        parsed.update(start_match_dict)
        start_binary = full_binary[start_match.start():start_match.end()]
    else:
        start_match_dict = {}
        start_binary = full_binary[0:DEFAULT_START_SIZE]

    end_expression = get_end_expression(parsed, output_type)
    end_match = end_expression.search(full_binary, DEFAULT_START_SIZE, len(full_binary))
    end_matched = end_match is not None

    if(end_matched):
        end_match_dict = end_match.groupdict()
        parsed.update(end_match_dict)
        end_binary = full_binary[end_match.start():end_match.end()]
    else:
        end_match_dict = {}
        end_binary = full_binary[DEFAULT_START_SIZE:DEFAULT_START_SIZE + DEFAULT_END_SIZE]

    if pre_process is not None:
        pre_process(parsed)

    if(start_matched or end_matched):
        for key in parsed.keys():
            if(key == "record_offset"):
                output["offsets"][key] = parsed[key]
                output["widths"][key] = parsed[key]
                output["stage0"][key] = parsed[key]
                output["stage1"][key] = parsed[key]

            elif(key in tables[output_type].keys() and
                    parsed[key] is not None):
                offset = None
                if key in start_match_dict.keys():
                    groupindex = start_expression.groupindex[key]
                    offset = start_match.start(groupindex) - DEFAULT_START_SIZE
                elif key in end_match_dict.keys():
                    groupindex = end_expression.groupindex[key]
                    offset = end_match.start(groupindex) - DEFAULT_START_SIZE

                output["offsets"][key] = offset
                output["widths"][key] = len(parsed[key])
                output["stage0"][key] = buffer(parsed[key])
                if(key == "message_id"):
                    output["stage1"][key] = unpack_message_id(parsed)
                if (key == "thread_id"):
                    output["stage1"][key] = unpack_thread_id(parsed)

                if(key == "sim"):
                    output["stage1"][key] = parsed[key] is not None
                elif(tables[output_type][key] == "SMALLINT"):
                    output["stage1"][key] = struct.unpack("<h", parsed[key])[0]
                elif(tables[output_type][key] == "INT" or
                        tables[output_type][key] == "INTEGER"):
                    output["stage1"][key] = struct.unpack("<i", (parsed[key] + "\x00\x00\x00\xFF")[:4])[0]

                elif (tables[output_type][key] == "INT8"):
                    output["stage1"][key] = struct.unpack("<q", parsed[key])[0]
                elif (tables[output_type][key] == "VARCHAR(1)"):
                    output["stage1"][key] = struct.unpack("c", parsed[key])[0]
                elif (tables[output_type][key] == "TEXT"):
                    try:

                        t = parsed[key].decode('utf-16le').encode('ascii', 'xmlcharrefreplace')
                        output["stage1"][key] = t
                        query = "SELECT str FROM dictionary WHERE str = :str LIMIT 1;"
                        params = {"bin_value": buffer(parsed[key]), "str": t}
                        cursor.execute(query, params)
                        if(cursor.fetchone() is None):
                            query = r"INSERT INTO dictionary(bin_value, str) VALUES (:bin_value, :str);"
                            cursor.execute(query, params)
                    except Exception as e:
                        pass
                else:
                    output["stage1"][key] = output["stage1"][key]

    fb = buffer(start_binary + end_binary)

    if(post_process is not None):
        post_process(parsed)
    cursor.execute(r'''
      INSERT INTO %s_full_binaries(record_offset, full_binary) VALUES (:record_offset, :full_binary);
    ''' % output_type, {"record_offset": hit, "full_binary": fb})
    db.commit()
    insert(output, output_type)
    return (start_matched, end_matched)


def type1_pre_process(parsed):
    try:
        if(parsed["message_id"] is None or len(parsed["message_id"]) < 4):
            parsed["message_id"] = parsed["message_id"]["id0"] + parsed["message_id"]["id1"] + "\x00\x00"
    except TypeError as e:
        pass
    try:
        if (parsed["thread_id"] is None or len(parsed["thread_id"]) < 4):
            parsed["thread_id"] = parsed["thread_id"]["tid0"] + parsed["thread_id"]["tid1"] + "\x00\x00"
    except TypeError as e:
        pass


def insert(output, table_id):
    """

    :param output:
    :type output: dict[str, dict[str, object]]
    :return:
    :rtype: int
    """
    global OUTPUT_TEMPLATES
    global cursor
    global db
    keys = OUTPUT_TEMPLATES[table_id].keys()

    query = """
              INSERT INTO %s_%%s(%s)
              VALUES (:%s);
            """ % (table_id, ", ".join(keys), ", :".join(keys))
    for sms_type in output.keys():
        try:
            q = query % sms_type
            cursor.execute(q, output[sms_type])
        except Exception as e:
            db.rollback()
            print("%r at %r" % (output[sms_type]["record_offset"], e))
            return -1

    db.commit()
    return 0
