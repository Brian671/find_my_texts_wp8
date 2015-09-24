import re

__author__ = 'Chris Ottersen'

exp_template = re.compile(
    r"""
        ^
        (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
        #.*?
        \x01
        (?P<content>
            (?:
                (?P<phone_1>(?:..){,20}?\x00\x00)\x01
                (?P<phone_2>(?:..){,20}?\x00\x00)\x01
                (?P<phone_3>(?:..){,20}?\x00\x00)\x01
            ){%s}
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
        (?<!\*{8,})
""", re.DOTALL | re.VERBOSE)


exp_incoming = re.compile(exp_template.pattern % "1", re.DOTALL | re.VERBOSE)
exp_outgoing = re.compile(exp_template.pattern % "0", re.DOTALL | re.VERBOSE)
exp_general  = re.compile(exp_template.pattern % "0,1", re.DOTALL | re.VERBOSE)
