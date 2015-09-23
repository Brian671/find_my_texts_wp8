import sqlite3
from datetime import datetime
import re

__author__ = 'Chris Ottersen'

''' :type : list[int] '''
x = [0, 0]


def create_expression(sequences, limit=4, dropnz=True):
    """

    :param sequences:
    :type sequences: dict[str, dict]
    :param limit:
    :type limit: int
    :param dropnz:
    :type dropnz: bool
    :return:
    :rtype: str
    """
    assert isinstance(sequences, dict)
    result_pattern = r""
    discard = limit != 0

    if len(sequences.keys()) != 0 and limit >= 0:
        lst = []
        for key in sequences.keys():

            if dropnz and key == r'\x00':
                continue
            p = create_expression(sequences[key], limit - 1, False)
            if p is not None:
                lst.append(r"%s%s" % (key, p))
                discard = False

        result_pattern = r"|".join(sorted(lst))
        if len(lst) > 1:
            result_pattern = r"(?:%s)" % result_pattern
    if discard:
        result_pattern = None
    return result_pattern

cursor = None
db = None
try:
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect('database/data/mydb')
    # Commit the change
    db.commit()
    cursor = db.cursor()
    cursor.execute(
        """
            SELECT record_offset, full_binary
            FROM sms_type0_stage0
            WHERE message_id IS NULL AND message IS NULL;
        """)

    unparsed = cursor.fetchall()
    print(len(unparsed))

    cursor.execute(
        """
            SELECT s0.record_offset, s0.message
            FROM sms_type0_stage0 as s0, sms_type0_stage1 as s1
            WHERE s1.message_id IS NOT NULL
            AND s1.message IS NOT NULL
            AND LENGTH(s0.message) > 0
            AND s0.record_offset = s1.record_offset;
        """)
    parsed = cursor.fetchall()
    db.commit()
    expression_chunks = []
    chunk_to_records = {}
    record_to_chunks = {}
    size = 5
    paths = [dict() for i in range(0, size)]
    count = 0
    stime = datetime.now()
    last_update = stime

    from_char = {}

    for i in range(0, len(parsed)):
        recent = [paths[0] for x in range(0, size)]

        (offset, bts) = parsed[i]
        text = str(bts)
        for j in range(0, len(text)):
            for k in range(0, len(recent)):

                char = r"\x%02x" % ord(text[j])

                if char not in recent[k].keys():
                    d = {}
                    recent[k][char] = d
                    if char not in from_char.keys():
                        from_char[char] = d

                recent[k] = recent[k][char]
    print(from_char)
    partial_expression = re.compile(create_expression(from_char, 3), re.DOTALL)
    counter = 0
    for (record_offset, full_binary) in unparsed:

        matches = []
        itr = partial_expression.finditer(str(full_binary))

        for match in itr:
            matches.append(match.group(0).replace('\x00', ''))

        print("%d:%r" % (record_offset, matches))
    exp = re.compile(r'\\x([a-zA-Z0-9]{2})')

    print(len(parsed))

# Catch the exception
except sqlite3.DatabaseError as e:
    # Roll back any change if something goes wrong
    if db is not None:
        db.rollback()
    raise e
finally:

    # Close the db connection
    db.close()
