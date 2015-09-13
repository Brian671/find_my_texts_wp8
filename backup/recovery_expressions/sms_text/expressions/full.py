__author__ = 'owner'
import re
# TODO: identify - deleted
# TODO: identify - location
# TODO: identify -
exp = re.compile(
    r"""
        (?:
            (?:
                (?P<u0>.{9})
                (?P<message_id>.{4})
                \x07\x00\x00\x00
                .{74}(?P<u1>.{4})(?P<thread_id>.{4})           # while not thoroughly tested, this seems to indicate the thread
                .{30}
            )?
            .{4}(?P<u2>.{4})                  # unknown
            .{42}
        )?(?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)          # unknown meaning
        .{6,36}(?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)          # unknown meaning

        (?P<direction>
            (?P<unread> \x00\x00\x00\x00)|
            (?P<read>   \x01\x00\x00\x00)|
            (?P<sent>   \x21\x00\x00\x00)|
            (?P<draft>  \x29\x00\x00\x00)|
            (?P<unknown_status>.{4})
         )
        .{4}(?P<u3>.{36}).{4}(?P<u4>.{4})
        (?P<u5>.{8})

        .{4}(?P<u6>.{4})
        .{20}(?P<u7>.{4})
        .{16}(?P<u8>.{6})
        .{12}(?P<u9>.{4})
        .{50}(?P<u10>.{4})(?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
        (?P<u11>
            (?P<u11a>.+?)\x00\x00\x01
            (?(draft)|(?(sent)|
                (?P<phone_0>(?:..)+?\x00\x00)\x01
            ))
        )

        # u"IPM.SMStext\0" marker identified in initial search
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)\x01

        # phone numbers (if present) and message. Both are captured in content so that if none are present
        (?P<content>                                                                        #

            (?(phone_0)
                (?P<phone_1>(?:..)+?\x00\x00)\x01
                (?P<phone_2>(?:..)+?\x00\x00)\x01
                (?P<phone_3>(?:..)+?\x00\x00)\x01
            |)?

            (?P<message>(?:..)+?)(?:\x00\x00)?
        )
        (?<=\x00\x00)
        (?:\x01
        (?P<u12>.{10})                                                                      #
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)                                                 # sent / recieved time
            (?:\x01(?P<sim>S\x00I\x00M\x00\x00\x00))?
        )
    """, re.DOTALL | re.VERBOSE)
