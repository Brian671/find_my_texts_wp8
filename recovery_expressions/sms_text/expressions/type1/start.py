__author__ = 'owner'
import re

start0 = re.compile(
    r"""

        (?P<u0>
            (?P<s0_marker>
                (?P<backwards_FILETIME_1>\x7F\x81(?P<t6>[\xCD-\xD9])(?P<t5>.)(?P<t4>.)(?P<t3>.)(?P<t2>.)(?P<t1>.)(?P<t0>.)\x7F\x80\x00)
                (?P<backwards_message_id>(?P<i1>.)(?P<i0>.))
            )
            (?:
                .{,500}?
                (?P=s0_marker)
            ){,10}?
            .{,500}?
        )
    """, re.DOTALL | re.VERBOSE)


def correct_FILETIME(backwards):
    return "%s\x01" % backwards[-3:1:-1]


def get_start1(FILETIME_1):
    return re.compile(
        r"""

            (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)
            \xDA\x20\x08
            (?P<FILETIME_1>%s)

            (?P<u1>.{,200}?)                                                                     # TODO: research

            \x5E\x21\x0B\xFC\xFF\xF7\xFF\xFF\x7D\xFE\x4F\xDF\x73\xFE\x69

            (?P<u2>.{,200}?)                                                                     # TODO: research

            (?:\x78\x41\x1B\x01(?P<phone_0>(?:..){,20}?\x00\x00))?
            \x78\x01\x19\x13\x01
        """ % FILETIME_1, re.DOTALL | re.VERBOSE)
