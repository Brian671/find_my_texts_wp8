__author__ = 'Chris Ottersen'
import sqlite3
from pytz import timezone
from datetime import *
from sqlite3 import Cursor, Connection

import re
from __builtin__ import str, long

TIME_ZONE_NAME = 'US/Pacific-New'
TIME_ZONE = timezone(TIME_ZONE_NAME)

db = sqlite3.connect(
    r"C:\Users\owner\Desktop\UFED_Extractions\Nokia GSM Lumia 520.2 (RM-915) 2015_07_28 (004)\Physical 02\data\mydb")
''' :type : sqlite3.Connection '''

cursor = db.cursor()
''' :type : sqlite3.Cursor '''


def filetime(num, format="%a %b %d %Y %H:%M:%S.%f{zepto} GMT%z (%Z)"):
    """
    Note {`zepto <https://en.wikipedia.org/wiki/Zepto->`_} is the last digit of the timestamp. It is usually rounded off.

    :param num:
    :type num: long
    :param format: str
    :type format: str
    :return:
    """
    global TIME_ZONE
    stamp = None
    time_obj = None
    if num is not None:
        x = (num - 116444736000000000) // 10000000
        time_obj = datetime.fromtimestamp(x, TIME_ZONE).replace(microsecond=(num % 10000000)/10)
        stamp = time_obj.strftime(format).format(zepto=num % 10)
    return stamp#, time_obj, num



def trim_blob(x, start_offset, end_offset):
    """
    Note {`zepto <https://en.wikipedia.org/wiki/Zepto->`_} is the last digit of the timestamp. It is usually rounded off.

    :param x:
    :type x: buffer
    :param start_offset:
    :type start_offset: int
    :param end_offset:
    :type end_offset: int
    :return:
    """
    temp = str(x)
    temp = temp[start_offset:end_offset]
    temp = buffer(temp)
    print ("before: %d - after: %d" % (len(x), len(temp)))
    print ("before: %r - after: %r" % (type(x), type(temp)))

    return temp


def execute_file(cursor, name):
    """



        :param cursor:
        :type cursor: Cursor
        :param name:
        :type name: str
        :rtype : None
    """
    f = open(name)
    cursor.executescript(f.read())
    f.close()

    return None


db.create_function("filetime", 1, filetime)
#  db.create_function("trim_blob", 3, trim_blob)

print filetime(0x01C7FE1531D203FF)

execute_file(cursor, "conversation_type0.sql")
execute_file(cursor, "sms_message_type0.sql")
execute_file(cursor, "sms_message_type1.sql")
execute_file(cursor, "sms_message_type2.sql")
execute_file(cursor, "final_product.sql")

#execute_file(cursor, "test.sql")
db.commit()

db.close()
