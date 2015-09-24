import re

__author__ = 'Chris Ottersen'

exp = re.compile(r"""
    ^
    \x01\x30\x00\xE1\xE0
    (?P<phone_1>(?:..){,20}?)\x00\x00\x01
    (?P<phone_2>(?:..){,20}?)\x00\x00\x00*?\x01
    (?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)?

""", re.DOTALL | re.VERBOSE)