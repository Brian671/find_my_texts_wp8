# find_my_texts_wp8
This is a utility to recover deleted SMS messages from a Windows 8.0 phone

I have discovered at least 4 distinct storage schema for SMS messages on a Nokia Lumia Windows 8.0 phone

```python
    (?P<u0>.{9})
    (?P<message_id>.{4})
    .{4}
    \*{45}                          
    (?:.{43})?
    \*{25}
    (?:.{43})?
    \*{4}                          
    
    (?P<u1>.{4})                   
    (?P<thread_id>.{4})           
    \*{34}
    (?P<u2>.{4})?                  
    \*{42}                          
    (?P<FILETIME_0>.{6}[\xCD-\xD9]\x01)          
    \*{36}
    (?P<FILETIME_1>.{6}[\xCD-\xD9]\x01)          
    
    (?P<direction>
        (?P<unread> \x00\x00\x00\x00)|
        (?P<read>   \x01\x00\x00\x00)|
        (?P<sent>   \x21\x00\x00\x00)|
        (?P<draft>  \x29\x00\x00\x00)|
        (?P<unknown_status>.{4})
    )
    \*{4}                                    
    (?P<u3>.{36})                           
    \*{4}                                    
    
    (?P<u4>.{4})                            
    (?P<u5>.{8})                            
    \*{4}                                    
    (?P<u6>.{4})                            
    
    \*{18}                                   
    (?P<u7>.{4})                            
    
    \*{16}                                   
    (?P<u8>.{6})                            
    
    \*{8}                                    
    (?P<u9>.{4})                          
    (?:
        .{50}
        (?P<u10>\x00\x00\x00\x00)
        (?P<FILETIME_2>.{6}[\xCD-\xD9]\x01)
    )?
    (?P<u11>
        (?P<u11a>.{,150}?)\x00\x00\x01
        (?(draft)\x00\x00|(?(sent)\x00\x00|
            (?:(?P<phone_0>(?:..){,20}?\x00\x00)\x01)?
        ))
    )
    (?P<SMStext>I\x00P\x00M\x00\.\x00S\x00M\x00S\x00t\x00e\x00x\x00t\x00\x00\x00)
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
```
    
## Current version
1. Reads the most common, known SMS storage format and places data in a SQLite DB
2. comments incomplete
