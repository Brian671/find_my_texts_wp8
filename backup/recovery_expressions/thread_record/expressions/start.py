__author__ = 'owner'
import re

exp = re.compile(r"""
    \x05\x00\x7F\x80\x00
    (?P<id_short>.(?P<id_byte>.))
    \x0C\x7F\x38\x00
    (?P<thread_id>....)
    \x07\x00\x00\x00\*{4}
    (?P<thread_length>.{4})
    (?P<u0>.{20})
    (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)
    (?P<message_count>.)
    (?P<u1>.{,160}?)
    (?:\x01(?P<phone_0>(?:..)+?))?
    $
""", re.DOTALL | re.VERBOSE)