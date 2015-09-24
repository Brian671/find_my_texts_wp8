import re

__author__ = 'Chris Ottersen'


exp_template = r"""
        ^
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        (?P<content>
            (?:
                \x8B\x41.\x01
                (?P<phone_2>(?:..){,20}?\x00\x00)
                \x8B\x41.\x01
                (?P<phone_3>(?:..){,20}?\x00\x00)
                \x8B\x41.\x01
                (?P<phone_4>(?:..){,20}?\x00\x00)
            ){%s}
            \x8B.(?P<message_length>.{,4}?)\x01
            (?P<message>(?:..){,500}?\x00\x00)
            \x8B\x41.\x01

        )

        (?P<u4>.{,25}?)
        (?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
        (?:
            .*?
            (?P<s1_marker>(?P<backwards>%s)(?P<ufoa1>.)(?P<ufoa0>.))
            .*?
            (?P=s1_marker)
            .*?
            (?P<FILETIME_3>.{6}[\xCD-\xD9]\x01)

            (?:
                (?:
                    # TODO: thread id
                    .*?
                    (?P<id_in>(?P<id0a>%s)(?P<id1a>%s)..)
                    .{4}
                    (?P<FILETIME_4>.{6}[\xCD-\xD9]\x01)
                    .{10}
                    (?P<phone_5>(?:..){,20}?\x00\x00)
                    \x01
                    (?P<phone_6>(?:..){,20}?\x00\x00)
                    .*?
                    (?P<s2_marker>
                        (?P=backwards)
                        (?P<ufo1b>.)
                        (?P<ufo0b>.)
                    )
                    .*?
                    (?P=s2_marker)
                ){%s}
                (?:
                    .*?
                    (?P<s3_marker>(?P=backwards)(?P<tid1>.)(?P<tid0>.))
                    .*?
                    (?P=s3_marker)
                    .*?
                    (?P=s3_marker)
                    .*?
                    (?P=s3_marker)
                    .*?
                    (?P<FILETIME_5>.{6}[\xCD-\xD9]\x01)
                    \x30\x20\x04
                    (?P<message_id>(?(id_in)(?P=id_in)|%s..))
                    .*?

                    (?:
                        # should be followed with id
                        .*?
                        (?P=backwards)  # TODO: add id to end
                        .*?
                        (?P=backwards)
                        .*?
                        (?P=backwards)
                        .*?
                        (?P<thread_id>(?P=tid0)(?P=tid1)..)
                        \x5E\x21\x0B\xFC\xFF\xE7\xFF\xFF\x7D\xFE\x4F\xDF\x73\xFE\x06
                    )?
                )?
            )?
        )?
    """


def get_end(phone_1=None, i0=None, i1=None, backwards=r"\x7F\x81[\xCD-\xD9]......\x7F\x80\x00"):
    """


    :param phone_1:
    :param i0:
    :param i1:
    :param backwards:
    :return:
    :rtype:
    """
    global exp_template

    if i0 is not None:
        i0 = r"\x%02X" % ord(i0)
    else:
        i0 = '.'

    if i1 is not None:
        i1 = r"\x%02X" % ord(i1)
    else:
        i1 = '.'
    if (phone_1 is not None):
        has_phone = "1"
    else:
        has_phone = "0,1"

    return re.compile(exp_template % (
        has_phone,
        backwards,
        i0,
        i1,
        has_phone,
        i0 + i1,
        #i1,
        #i0
    ),
    re.DOTALL | re.VERBOSE)
