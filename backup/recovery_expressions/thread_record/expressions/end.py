__author__ = 'owner'

import re

exp = re.compile(r"""
    ^
    \x01\x30\x00\xE1\xE0
    (?P<phone_1>(?:..){,160}?)\x00\x00\x01
    (?P<phone_2>(?:..){,160}?)\x00\x00\x00*\x01
    (?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)

""", re.DOTALL | re.VERBOSE)