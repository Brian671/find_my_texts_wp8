import re

__author__ = 'Chris Ottersen'


exp = re.compile(
    r"""

        (?!.*I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        (?:
            (?:
                (?:
                    (?P<u0>.{8})
                    (?P<message_id0>....)
                    (?P<u1>.{12})
                    (?P<FILETIME_0>......[\xCD-\xD9]\x01)

                    (?P<u2>.{88})
                    (?P<direction>
                        (?P<unread> \x00\x00\x00\x00)|
                        (?P<read>   \x01\x00\x00\x00)|
                        (?P<sent>   \x21\x00\x00\x00)|
                        (?P<draft>  \x29\x00\x00\x00)|
                        (?P<unknown_status>.{4})
                    )
                )
                (?P<u3>.{44})
                (?P<FILETIME_1>......[\xCD-\xD9]\x01)

                (?P<u4>.{24})
                (?P<FILETIME_2>......[\xCD-\xD9]\x01)

                (?P<u5>.{84})
                \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x00\x15\x30\x00\x00\x00\x00
            )?

            (?P<thread_id>....)
            (?P<u6>.{36})
            \x40\x00\x19\x83\x00\x00\x00\x01\x00\x00\x00\x00
            \x00\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x00
            (?P<message_id>....)
            \x00\x00\x00\x00\x03\x00\x02\x00\x00\x00\x00\x00
        )
        (?P<u7>.{4})
        \x00{4,}
        (?(sent)|(?(draft)|
            (?P<phone_0>(?:..)*?)
            \x00\x00
            (?:\x00{2})+
        ))?
        (?:(?P<message>(?:..)+)\x00\x00)
        (?:\x00{2}){1,4}
        $
""", re.DOTALL | re.VERBOSE)
