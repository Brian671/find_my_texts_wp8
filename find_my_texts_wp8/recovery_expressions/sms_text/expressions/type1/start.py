import re

__author__ = 'Chris Ottersen'


exp = re.compile(
    r"""
        (?:
            (?:
                \*{162}
                (?P<FILETIME_7>.{6}[\xCD-\xD9]\x01)
                \*{44}
                .{4}
                \*{82}
                .{4}
                \*{18}
                .{4}
                \*{18}
                .{4}
                \*{10}
                .{28}
                \x01I\x00P\x00M\x00\.\x00N\x00o\x00t\x00e\x00\x00\x00
                (?P=FILETIME_7)
                (?!.*\x01I\x00P\x00M\x00\.\x00N\x00o\x00t\x00e\x00\x00\x00)
                .*?

            )?
            #####################################################
            (?P<SMS>
                (?P<FILETIME_6>
                    (?P<smst0>.)
                    (?P<smst1>.)
                    (?P<smst2>.)
                    (?P<smst3>.)
                    (?P<smst4>.)
                    (?P<smst5>.)
                    (?P<smst6>[\xCD-\xD9])\x01
                )
                .{25}
                \x40\x01\x53\x00\x4D\x00\x53\x00\x00\x00\x01
                #(?P<phone_0>(?:..){,20}?(?P<p0>(?:..)?)(?P<p1>(?:..)?)(?P<p2>(?:..)?)(?P<p3>(?:..)?)(?P<p4>(?:..)?)(?P<p5>(?:..)?)\x00\x00)
                #\x01(?P=p5)(?P=p4)(?P=p3)(?P=p2)(?P=p1)(?P=p0)\x00\x00
                (?P<phone_0>(?:..){,20}?\x00\x00)\x01
                (?P<phone_0r>(?:..){,6}\x00\x00)?
                .*?
                (?P<backwards_FILETIME_6>\x7F\x81(?P=smst6)(?P=smst5)(?P=smst4)(?P=smst3)(?P=smst2)(?P=smst1)(?P=smst0)\x7F\x80\x00)
                .*?
                (?P=backwards_FILETIME_6)
                (?!.*\x40\x01\x53\x00\x4D\x00\x53\x00\x00\x00\x01)
                .*?
            )
        )?
        #####################################################
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

        (?:\x78\x41\x1B\x01(?P<phone_1>(?:..){,20}?\x00\x00))?
        \x78\x01\x19\x13\x01
        $
        """, re.DOTALL | re.VERBOSE)


def preprocess():
    r"""\x40\x01\x53\x00\x4D\x00\x53\x00\x00\x00\x01(?P < phone_0 > (?:..){, 20}?\x00\x00)
    .* ?"""
    pass
