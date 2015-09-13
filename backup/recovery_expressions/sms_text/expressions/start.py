__author__ = 'owner'
import re
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
        )$
""", re.DOTALL | re.VERBOSE)
