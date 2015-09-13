__author__ = 'owner'
import re
# TODO: identify - deleted
# TODO: identify - location
# TODO: identify -
exp = re.compile(
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

        (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)
        \xDA\x20\x08
        (?P<FILETIME_1>(?P=t0)(?P=t1)(?P=t2)(?P=t3)(?P=t4)(?P=t5)(?P=t6)\x01)

        (?P<u1>.{,200}?)                                                                     # TODO: research

        \x5E\x21\x0B\xFC\xFF\xF7\xFF\xFF\x7D\xFE\x4F\xDF\x73\xFE\x69

        (?P<u2>.{,200}?)                                                                     # TODO: research

        (?:\x78\x41\x1B\x01(?P<phone_0>(?:..){,20}?\x00\x00))?
        \x78\x01\x19\x13\x01
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


        (?P<u4>.{,25}?)
        (?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
        (?:(?:
        # !! EXPRESSION FAILS HERE !!
        (?P<u5>
            .{,500}?
            (?P<s1_marker>(?P=backwards_FILETIME_1)(?P<backwards_message_uid>(?P<uid1>.)(?P<uid0>.)))
            (?:
                .{,500}?
                (?P=s1_marker)
            ){,10}?
            .{,500}?
            |.{,1500}?
        )


        (?P<u6>
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)
            .{,500}?
            (?P<s2_marker>(?P=backwards_FILETIME_1)(?P<backwards_message_id>(?P<tid1>.)(?P<tid0>.)))
            (?:
                .{,500}?
                (?P=s2_marker)
            ){,10}?
            .{,500}?
            |.{,1500}?
        )


        (?P<u7>
            (?P<FILETIME_4>.{6}[\xCD-\xD9]\x01)
            \x30\x20\x04
            (?P<message_id>(?=id0)(?=id1)..)
            (?:
                .{,500}?
                (?P=s0_marker)
            ){,10}?
            .{,500}?
            |.{,1500}?
        )
        )|.+)
        (?:#(?=tid0)(?=tid1)
            (?P<thread_id>....)
            \x5E\x21\x0B\xFC\xFF\xE7\xFF\xFF\x7D\xFE\x4F    #^!......}.O.s..
        )?
    """, re.DOTALL | re.VERBOSE)
