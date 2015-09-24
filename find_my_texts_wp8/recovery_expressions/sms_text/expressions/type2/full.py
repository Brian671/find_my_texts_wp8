import re

__author__ = 'Chris Ottersen'

# TODO: identify - deleted
# TODO: identify - location
# TODO: identify -

x='''
exp = re.compile(
    r"""

        .{7}
        (?P<message_id1>.{4})
        .
        (?P<FILETIME_2>.{6}[[\xCD-\xD9]\x01])
        .{67}
        (?P<message_id0>.{4})
        .{12}
        (?P<message_id>.{4})
        .
        (?P<direction>
            (?P<unread> \x00\x00\x00\x00)|
            (?P<read>   \x01\x00\x00\x00)|
            (?P<sent>   \x21\x00\x00\x00)|
            (?P<draft>  \x29\x00\x00\x00)|
            (?P<unknown_status>.{4})
        )
        .{44}
        (?P<FILETIME_1>.{6}[[\xCD-\xD9]\x01])
        .{3}
        (?P<message_id>.{4})
        .{17}
        (?P<FILETIME_0>.{6}[[\xCD-\xD9]\x01])
        .{104}
        (?P<thread_id1>.{4})
        .{4}
        (?P<thread_id>(?(thread_id0)(?P=thread_id1)|.{4})
        .{49}

        (?P<message_id>.{4})
        .{20}
        (?P<content>
            (?(draft)|(?(sent)|
                (?P<phone_0>(?:..){,20}?\x00\x00)\x00\x00
            ))
            (?P<message>(?:.(?:(?:(?<!.).)|[^\x00])*?)?(?:\x00\x00))?
        )
        .{4}
        (?<!I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        $

    """, re.DOTALL | re.VERBOSE)
'''