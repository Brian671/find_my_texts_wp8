import re
exp = re.compile(
    r"""

        (?:
            (?P<FILETIME_6>
                (?P<smst0>.)
                (?P<smst1>.)
                (?P<smst2>.)
                (?P<smst3>.)
                (?P<smst4>.)
                (?P<smst5>.)
                (?P<smst6>[\xCD-\xD9])\x01
            )
            .{20,30}?
            \x40\x01\x53\x00\x4D\x00\x53\x00\x00\x00\x01(?P<phone_0>(?:..){,20}?\x00\x00)
            .*?
            (?P<backwards_FILETIME_6>\x7F\x81(?P=smst6)(?P=smst5)(?P=smst4)(?P=smst3)(?P=smst2)(?P=smst1)(?P=smst0)\x7F\x80\x00)
            .*?
            (?P=backwards_FILETIME_6)
            .*?
        )
    """, re.DOTALL | re.VERBOSE)