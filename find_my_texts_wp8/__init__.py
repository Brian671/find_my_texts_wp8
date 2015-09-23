__author__ = 'owner'
__version__ = '__init__.py v2015-09-22'

#from find_my_texts_wp8 import parse_thread as parse_thread
#from find_my_texts_wp8 import parse_sms as parse_sms
#from find_my_texts_wp8 import database as database

from find_my_texts_wp8.recovery_expressions.thread_record.parse import parse_thread as parse_thread
from find_my_texts_wp8.recovery_expressions.sms_text.parse import parse_sms as parse_sms
from find_my_texts_wp8.database import sms_database
import struct
import pydoc
# TODO: check into Smil.txt
# TODO: IPM.Note
# TODO: IPM.MSG
# TODO: IPM.MMS
# TODO: map type 2
# TODO: map type 3
# TODO: parse sms


# TODO: message 14 - bad text
# TODO: message 17 - bad text
# TODO: message 21 - bad text
# TODO: message 25 - bad text

# TODO: message 35 - missed
# TODO: message 42 - missed
# TODO: message 47 - missed

# TODO: message 11 - phone number missed
# TODO: message 53 - phone number missed

# TODO: message 43- weird chars

# TODO: general - does not handle multiple parties
# TODO: localize timezones
