import re

__author__ = 'Chris Ottersen'

exp_success = re.compile(
    r"""
        ^
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        (?P<u9>.{52,}?)
""", re.DOTALL | re.VERBOSE)

exp_fail = re.compile(".^", re.DOTALL | re.VERBOSE)
