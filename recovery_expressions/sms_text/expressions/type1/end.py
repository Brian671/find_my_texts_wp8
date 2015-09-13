__author__ = 'owner'

import re

end0 = re.compile(
    r"""
        ^
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        (?P<content>
            (?(phone_0)
                \x8B\x41\x1B\x01
                (?P<phone_1>(?:..){,20}?\x00\x00)
                \x8B\x41\x1B\x01
                (?P<phone_2>(?:..){,20}?\x00\x00)
                \x8B\x41\x1B\x01
                (?P<phone_3>(?:..){,20}?\x00\x00)
            )?
            \x8B.(?P<message_length>.{,4}?)\x01
            (?:(?P<message>(?:..){,500}?)(?=\x00\x00))(?:\x00\x00)?
        )
    """, re.DOTALL | re.VERBOSE)

end1 = re.compile(
    r"""
        ^
        (?P<u4>.{,25}?)
        (?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
    """, re.DOTALL | re.VERBOSE)


def get_end2(backwards):
    return re.compile(
        r"""
            ^
            .{,500}?
            (?P<s1_marker>%s(?P<backwards_message_uid>(?P<uid1>.)(?P<uid0>.)))
            (?:
                .{,500}?
                (?P=s1_marker)
            ){,10}?
            .{,500}?
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)

        """ % backwards, re.DOTALL | re.VERBOSE)


def get_end3(backwards):
    return re.compile(
        r"""
            ^
            .{,500}?
            (?P<s2_marker>%s(?P<backwards_message_id>(?P<tid1>.)(?P<tid0>.)))
            (?:
                .{,500}?
                (?P=s2_marker)
            ){,10}?
            .{,500}?
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)
            (?P<message_id>(?=id0)(?=id1)..)
        """ % backwards, re.DOTALL | re.VERBOSE)


def get_end4(marker):
    return re.compile(
        r"""
            ^
            (?:
                .{,500}?
                %s
            ){,10}?
            .{,500}?

        """ % marker, re.DOTALL | re.VERBOSE)


def get_end5(s0_marker):
    return re.compile(
        r"""

        (?P<message_id>(?=id0)(?=id1)..)
        (?P<u7>
            (?:
                .{,500}?
                %s
            ){,10}?
            .{,500}?
        )
        """ % s0_marker, re.DOTALL | re.VERBOSE)