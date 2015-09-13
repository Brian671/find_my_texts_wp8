__author__ = 'owner'
import re
# TODO: identify - deleted
# TODO: identify - location
# TODO: identify -
exp = re.compile(
    r"""
        (?P<u0>.{9})
        (?P<message_id>.{4})
        .{4}
        \*{45}                          #74
        (?:.{43})?
        \*{25}
        (?:.{43})?
        \*{4}                           #/74

        (?P<u1>.{4})                    #padding
        (?P<thread_id>.{4})           # while not thoroughly tested, this seems to indicate the thread
        \*{34}
        (?P<u2>.{4})?                  # unknown
        \*{42}                          #80
        (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)          # unknown meaning
        \*{36}
        (?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)          # unknown meaning

        (?P<direction>
            (?P<unread> \x00\x00\x00\x00)|
            (?P<read>   \x01\x00\x00\x00)|
            (?P<sent>   \x21\x00\x00\x00)|
            (?P<draft>  \x29\x00\x00\x00)|
            (?P<unknown_status>.{4})
        )
        \*{4}                                    #4
        (?P<u3>.{36})                           #40
        \*{4}                                    #44

        (?P<u4>.{4})                            #48
        (?P<u5>.{8})                            #56
        \*{4}                                    #60
        (?P<u6>.{4})                            #64

        \*{18}                                   #82-84
        (?P<u7>.{4})                            #14 00 00 00

        \*{16}                                   #****************
        (?P<u8>.{6})                            #00 00 00 00 00 00

        \*{8}                                    #********
        (?P<u9>.{4})                            #01 00 00 00
        (?:

            .{50}
            (?P<u10>\x00\x00\x00\x00)
            (?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
            #|
            #\x01\x00\x00\x00

        )?
        (?P<u11>
            (?P<u11a>.{,150}?)\x00\x00\x01
            (?(draft)\x00\x00|(?(sent)\x00\x00|
                (?:(?P<phone_0>(?:..){,20}?\x00\x00)\x01)?
            ))
        )
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        #.*?
        \x01
        (?P<content>
            (?(draft)|(?(sent)|
                (?:
                    (?P<phone_1>(?:..){,20}?\x00\x00)\x01
                    (?P<phone_2>(?:..){,20}?\x00\x00)\x01
                    (?P<phone_3>(?:..){,20}?\x00\x00)\x01
                )
            ))
            (?:(?P<message>(?:..)*?)?(?:\x00\x00))?
        )
        (?<=\x00\x00)
        (?:\x01
            (?:\x00\x00(?P<FILETIME_2b>.{6}[\xCD-\xD9]\x01)..)?
            (?P<u12>.{2,25}?)
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)
            (?:\x01
                (?P<sim>S\x00I\x00M\x00\x00\x00)
            )?
        )
    """, re.DOTALL | re.VERBOSE)
