"""
# The MPD store.vol Contact record structures for a Phonebook type entry look like one of the following:
# MPD format 1:
# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Name5][0x1][Phone1][0x1][Codestring][0x1][Phone2][0x1][Name6][0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
#
# Note: Above fields contain null-terminated Unicode strings and Codestring is something like "ABCH".
#
# MPD format 2:
# [?][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Name5][0x1][Phone1][0x1][Phone2][0x1][Name6][0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
#
# Note: Above fields contain null-terminated Unicode strings.
#
# The MPD Hotmail type entry (only one was found) is:
# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Codestring][0x1][0x8 bytes][0x1][Name5][0x1][Name6][0x1][Email][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
#
# Note: All fields except for the (binary) 0x8 bytes in the middle contain null-terminated Unicode strings
#
# The Garda Contact records appear to follow these 3 patterns:
# Garda format 1:
# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Name5][0x1][Phone1][0x1][Codestring][0x1][GUID][0x1][Phone2][0x1][Name6][0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
#
# Note: All fields above contain null-terminated Unicode strings. This is the same as MPD format 1 but with an additional GUID string.
#
# Garda format 2:
# [?][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Name5][0x1][Country][0x1][City][0x1][Phone1][0x1][handle][0x1][Phone2][0x1][Name6][0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# Note: Above Name strings contained non-Unicode characters in some instances. There was also a potential email handle field (eg "firstname.lastname").
#
# Garda format 3:
# [?][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Name5][0x1][Name6][0x1][Name7][0x1][Name8][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
#
"""
import re
__author__ = 'Christopher Ottersen'
__version__ = '__init__.py v2015-10-02'

# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4]                                 [0x1][Name5]                         [0x1][Phone1][0x1][Codestring]             [0x1][Phone2][0x1][Name6]            [0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# [?]                [0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4]                                 [0x1][Name5]                         [0x1][Phone1]                              [0x1][Phone2][0x1][Name6]            [0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4][0x1][Codestring][0x1][0x8 bytes][0x1][Name5]                                                                                 [0x1][Name6][0x1][Email]            [01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# [?][0x1][19 Digits][0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4]                                 [0x1][Name5]                         [0x1][Phone1][0x1][Codestring][0x1][ GUID ][0x1][Phone2][0x1][Name6]            [0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# [?]                [0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4]                                 [0x1][Name5][0x1][Country][0x1][City][0x1][Phone1]                 [0x1][handle][0x1][Phone2][0x1][Name6]            [0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]
# [?]                [0x1][Name1][0x1][Name2][0x1][Name3][0x1][Name4]                                 [0x1][Name5]                                                       [0x1][NameXX]             [0x1][Name6]            [0x1][Name7][01 04 00 00 00 82 00 E0 00 74 C5 B7 10 1A 82 E0 08]

mpd_format1 = re.compile(r"""



        (?!.*\x01\x04\x00\x00\x00\x82\x00\xE0\x00\x74\xC5\xB7\x10\x1A\x82\xE0\x08)
        #\x04\x00\x01\x00
        #(?P<u00>.{17})
        .+?
        \x01(?P<name_0>(?:..)*?\x00\x00)
        \x01(?P<name_1>(?:..)*?\x00\x00)
        \x01(?P<name_2>(?:..)*?\x00\x00)
        \x01(?P<name_3>(?:..)*?\x00\x00)
        (?P<u01>
            \x01(?P<Codestring>.*)
            \x01(?P<u02>.{8})
        )?
        \x01(?P<name_4>(?:..)*?\x00\x00)
        (?(u00)|
            (?P<u2>
                \x01(?P<country>(?:..)*?\x00\x00)
                \x01(?P<city>(?:..)*?\x00\x00)
            )?

            \x01(?P<phone_0>(?:..)*?\x00\x00)

        )


    """, re.DOTALL | re.VERBOSE)

'''
mpd_format1 = re.compile(r"""
        (?!.*\x01\x04\x00\x00\x00\x82\x00\xE0\x00\x74\xC5\xB7\x10\x1A\x82\xE0\x08)
        #\x04\x00\x01\x00
        #(?P<u00>.{17})
        .+?
        \x01(?P<name_0>(?:..)*?\x00\x00)
        \x01(?P<name_1>(?:..)*?\x00\x00)
        \x01(?P<name_2>(?:..)*?\x00\x00)
        \x01(?P<name_3>(?:..)*?\x00\x00)
        (?P<u01>
            \x01(?P<Codestring>.*)
            \x01(?P<u02>.{8})
        )?
        \x01(?P<name_4>(?:..)*?\x00\x00)
        (?(u00)|
            (?P<u2>
                \x01(?P<country>(?:..)*?\x00\x00)
                \x01(?P<city>(?:..)*?\x00\x00)
            )?

            \x01(?P<phone_0>(?:..)*?\x00\x00)

        )


    """, re.DOTALL | re.VERBOSE)
'''