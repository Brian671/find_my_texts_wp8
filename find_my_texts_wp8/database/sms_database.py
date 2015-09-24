import sqlite3  # Import the SQLite3 module

__author__ = 'Chris Ottersen'

''' :type : Connection | None '''
db = None
''' :type : Cursor | None '''
cursor = None

''' :type : dict[str, dict[str, str]] '''
tables = {
    "sms_type0": {
        "record_offset": "INTEGER PRIMARY KEY NOT NULL",
        "version":       "TEXT",
        "u0":            "BLOB",
        "message_id":    "INTEGER",
        "u1":            "BLOB",
        "thread_id":     "INTEGER",
        "u2":            "BLOB",
        "FILETIME_0":    "INT8",
        "FILETIME_1":    "INT8",
        "direction":     "INTEGER",
        "FILETIME_2":    "INT8",
        "u3":            "BLOB",
        "u4":            "BLOB",
        "u5":            "BLOB",
        "u6":            "BLOB",
        "u7":            "BLOB",
        "u8":            "BLOB",
        "u9":            "BLOB",
        "u10":           "BLOB",
        "u11":           "BLOB",
        "u11a":          "BLOB",
        "phone_0":       "TEXT",
        "SMStext":       "TEXT",
        "content":       "BLOB",
        "phone_1":       "TEXT",
        "phone_2":       "TEXT",
        "phone_3":       "TEXT",
        "message":       "TEXT",
        "FILETIME_2b":   "INT8",
        "u12":           "BLOB",
        "FILETIME_3":    "INT8",
        "sim":           "TEXT",
    },

    "sms_type1": {
        "record_offset": "INTEGER PRIMARY KEY NOT NULL",
        "version":       "TEXT",
        "u0":            "BLOB",
        "t0":            "VARCHAR(1)",
        "t1":            "VARCHAR(1)",
        "t2":            "VARCHAR(1)",
        "t3":            "VARCHAR(1)",
        "t4":            "VARCHAR(1)",
        "t5":            "VARCHAR(1)",
        "i1":            "VARCHAR(1)",
        "i2":            "VARCHAR(1)",
        "FILETIME_0":    "INT8",
        "FILETIME_1":    "INT8",
        "u1":            "BLOB",
        "u2":            "BLOB",
        "phone_0":       "TEXT",
        "SMStext":       "TEXT",
        "content":       "BLOB",
        "phone_1":       "TEXT",
        "phone_2":       "TEXT",
        "phone_3":       "TEXT",
        "phone_4":       "TEXT",
        "phone_5":       "TEXT",
        "phone_6":       "TEXT",
        "message":       "TEXT",
        "FILETIME_2":    "INT8",
        "u3":            "BLOB",
        "u4":            "BLOB",
        "u5":            "BLOB",
        "u6":            "BLOB",
        "u7":            "BLOB",
        "u8":            "BLOB",
        "FILETIME_3":    "INT8",
        "FILETIME_4":    "INT8",
        "FILETIME_5":    "INT8",
        "FILETIME_6":    "INT8",
        "FILETIME_7":    "INT8",
        "message_id":    "INTEGER",
        "thread_id":     "INTEGER",
    },
    "conversation_type0": {
        "record_offset": "INTEGER PRIMARY KEY NOT NULL",
        "version":       "TEXT",
        "thread_id":     "INTEGER",
        "thread_length": "INTEGER",
        "u0":            "BLOB",
        "FILETIME_0":    "INT8",
        "u1":            "BLOB",
        "phone_0":       "TEXT",
        "phone_1":       "TEXT",
        "phone_2":       "TEXT",
        "FILETIME_1":    "INT8",
        "full_binary":   "BLOB"
    }
}

"""
def windows_time_seconds(t):
    return t / 10000000 - 11644473600


def windows_time_fraction(t):
    return t / 10000000
"""


def create_type0table(database=None, curs=None):

    if database is None:
        global db
        database = db
    if curs is None:
        global cursor
        curs = cursor
    curs.execute(r"""DROP VIEW IF EXISTS message_process_s0;""")

    curs.execute(r"""
        CREATE VIEW message_process_s0 AS
        SELECT
          sms_type0_stage1.message_id             AS message_id,
          sms_type0_stage1.thread_id              AS thread_id,
          sms_type0_stage1.message                AS message,
          sms_type0_stage1.FILETIME_0             AS FILETIME_0,
          sms_type0_stage1.FILETIME_1             AS FILETIME_1,
          coalesce(sms_type0_stage1.FILETIME_2,
                   sms_type0_stage1.FILETIME_2b)  AS FILETIME_2,
          sms_type0_stage1.FILETIME_3             AS FILETIME_3,
          cast(sms_type0_stage0.direction as String)
                                                  AS sent_recieved_text,
          sms_type0_stage0.direction              AS sent_recieved_hex,
          sms_type0_stage1.phone_0                AS phone_0,
          sms_type0_stage1.phone_1                AS phone_1,
          sms_type0_stage1.phone_2                AS phone_2,
          sms_type0_stage1.phone_3                AS phone_3,
          threads.Phone                           AS phone_4,
          coalesce(
              sms_type0_stage1.phone_0,
              sms_type0_stage1.phone_1,
              sms_type0_stage1.phone_2,
              sms_type0_stage1.phone_3,
              threads.Phone
          )                                       AS Phone

        FROM threads AS threads, sms_type0_stage0 AS sms_type0_stage0, sms_type0_stage1 AS "sms_type0_stage1"
        WHERE threads.thread_id = sms_type0_stage1.thread_id AND sms_type0_stage0.record_offset = sms_type0_stage1.record_offset;

    """)

    curs.execute(r"""DROP VIEW IF EXISTS message_process_s1;""")

    curs.execute(r"""
        CREATE VIEW message_process_s1 AS
        SELECT message_id,
          thread_id,
          message,
          FILETIME_0,
          FILETIME_1,
          FILETIME_2,
          FILETIME_3,
          ((FILETIME_0 - 116444736000000000) / 10000000) AS unix_time0,
          ((FILETIME_1 - 116444736000000000) / 10000000) AS unix_time1,
          ((FILETIME_2 - 116444736000000000) / 10000000) AS unix_time2,
          ((FILETIME_3 - 116444736000000000) / 10000000) AS unix_time3,
          FILETIME_0 % 10000000 AS milliseconds0,
          FILETIME_1 % 10000000 AS milliseconds1,
          FILETIME_2 % 10000000 AS milliseconds2,
          FILETIME_3 % 10000000 AS milliseconds3,
          (CASE
            WHEN hex(sent_recieved_hex) LIKE '00%' THEN 'incoming (unread)'
            WHEN hex(sent_recieved_hex) LIKE '01%' THEN 'incoming (read)'
            WHEN hex(sent_recieved_hex) LIKE '21%' THEN 'outgoing (sent)'
            WHEN hex(sent_recieved_hex) LIKE '29%' THEN 'outgoing (unknown, possibly draft)'
            WHEN phone_0 IS NULL AND phone_1 IS NULL THEN 'outgoing (unknown)'
            ELSE 'incoming (unknown)'
          END)                   AS sent_recieved_text,
          sent_recieved_hex,
          Phone


        FROM message_process_s0;
    """)

    curs.execute(r"""DROP VIEW IF EXISTS message_intermediate;""")

    curs.execute(r"""
        CREATE VIEW message_intermediate AS
          SELECT

            message_id                                 AS message_id,
            thread_id                                  AS thread_id,

            NULLIF(printf('%s.%-07d',
                          strftime('%m-%d-%m-%Y %H:%M:%S',
                                   unix_time0,
                                   'unixepoch',
                                   'localtime'),
                          milliseconds0), '.0000000')    AS timestamp0,

            NULLIF(printf('%s.%-07d',
                          strftime('%m-%d-%m-%Y %H:%M:%S',
                                   unix_time1,
                                   'unixepoch',
                                   'localtime'),
                          milliseconds1), '.0000000')    AS timestamp1,

            NULLIF(printf('%s.%-07d',
                          strftime('%m-%d-%m-%Y %H:%M:%S',
                                   unix_time2,
                                   'unixepoch',
                                   'localtime'),
                          milliseconds2), '.0000000')    AS timestamp2,

            NULLIF(printf('%s.%-07d',
                          strftime('%m-%d-%Y %H:%M:%S',
                                   unix_time3,
                                   'unixepoch',
                                   'localtime'),
                          milliseconds3), '.0000000')  AS timestamp3,
            sent_recieved_text                         AS direction,
            hex(sent_recieved_hex)                     AS "direction (hex)",
            Phone                                      AS Phone,
            message                                    AS message
          FROM message_process_s1
          WHERE
            coalesce(message_id,
                     thread_id,
                     message,
                     FILETIME_0,
                     FILETIME_1,
                     FILETIME_2,
                     FILETIME_3,
                     sent_recieved_text,
                     Phone) IS NOT NULL

          GROUP BY message_id
          ORDER BY message_id DESC;
    """)


def generate_tables(name, primary_key=None, columns=None, database=None, curs=None):
    """

    :param name:
    :type name: str
    :param primary_key:
    :type primary_key: str | None
    :param columns:
    :type columns: str | None
    :param database:
    :type database: Connection | None
    :param curs:
    :type curs: Cursor | None
    :return:
    :rtype: (Connection, Cursor)
    """
    if database is None:
        global db
        database = db
    if curs is None:
        global cursor
        curs = cursor
    if columns is None:
        global tables
        columns = tables[name]
    sub_tables = {
        "widths": {k: "INT" for k in columns.keys()},
        "offsets": {k: "INT" for k in columns.keys()},
        "stage0": {k: "BLOB" for k in columns.keys()},
        "stage1": dict(columns)
    }
    if primary_key is not None:
        sub_tables["widths"][primary_key] = columns[primary_key]
        sub_tables["offsets"][primary_key] = columns[primary_key]
        sub_tables["stage0"][primary_key] = columns[primary_key]

    curs.execute("DROP TABLE IF EXISTS %s_full_binaries;" % name)
    curs.execute(r'''
      CREATE TABLE IF NOT EXISTS
      %s_full_binaries
      (
        record_offset INTEGER PRIMARY KEY NOT NULL,
        full_binary BLOB
      );
    ''' % name)

    database.commit()
    for table in sub_tables.keys():
        curs.execute("DROP TABLE IF EXISTS %s_%s;" % (name, table))

        query = '''
            CREATE TABLE %s_%s
            (
              %s
            );
        ''' % (name,
               table,
               ",\n              ".join([("%-20s %s" % (k, sub_tables[table][k])) for k in sub_tables[table].keys()]))
        curs.execute(query)
    database.commit()

    return (database, curs)


def init_db(db_path='database/data/mydb'):
    global db
    global cursor
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(db_path)
        # Get a cursor object
        cursor = db.cursor()
        generate_tables("sms_type0", "record_offset")
        generate_tables("conversation_type0", "record_offset")
        generate_tables("sms_type1", "record_offset")
        cursor.execute(r"DROP TABLE IF EXISTS dictionary;")
        cursor.execute(r'''
          CREATE TABLE
          dictionary
          (
            str TEXT PRIMARY KEY NOT NULL,
            bin_value BLOB
          );
        ''')
        db.commit()

    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        if db is not None:
            db.rollback()
        raise e
    finally:
        pass
        # Close the db connection
        # db.close()
    return db
