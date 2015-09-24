import re

__author__ = 'Chris Ottersen'

exp = re.compile(r"""
    #\x05\x00\x7F\x80\x00
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
""", re.DOTALL | re.VERBOSE)
