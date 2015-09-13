__author__ = 'owner'
import re

exp = re.compile(r"""
    #(?:\x04\x00\x01|\x00\x7F\x80)?\x00
    (?P<id_short>.?(?P<id_byte>.))
    #(?P<id_short>.(?P<id_byte>.))
    \x0C\x7F\x38\x00
    (?P<thread_id>....)
    .{4}
    \*{4}
    (?P<thread_length>.{4})
    (?P<u0>.{20})
    (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)
    (?P<message_count>.)
    (?P<u1>.{,200})
    (?:\x01(?P<phone_0>(?:.\x00){,20}?))?
    $
""", re.DOTALL | re.VERBOSE)