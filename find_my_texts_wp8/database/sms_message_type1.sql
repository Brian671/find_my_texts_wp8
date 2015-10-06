/*
for filetime:
NULLIF(printf('%s.%-07d',
strftime('%d-%m-%Y %H:%M:%S',
       ((FILETIME_0 - 116444736000000000) / 10000000),
       'unixepoch',
       'localtime'),
FILETIME_0 % 10000000), '.0000000')
as "FILETIME_0 (day-month-year hour:minute:seconds)"

*/





DROP VIEW IF EXISTS process_sms_type1_stage0;
CREATE VIEW process_sms_type1_stage0 AS
SELECT
  sms_type1_stage1.message_id             AS message_id,
  sms_type1_stage1.thread_id              AS thread_id,
  sms_type1_stage1.message                AS message,
  sms_type1_stage1.FILETIME_0             AS FILETIME_0,
  sms_type1_stage1.FILETIME_1             AS FILETIME_1,
  sms_type1_stage1.FILETIME_2             AS FILETIME_2,
  sms_type1_stage1.FILETIME_3             AS FILETIME_3,
  NULL                                    AS sent_recieved_text,
  sms_type1_stage1.phone_0                AS phone_0,
  sms_type1_stage1.phone_1                AS phone_1,
  sms_type1_stage1.phone_2                AS phone_2,
  sms_type1_stage1.phone_3                AS phone_3,
  sms_type1_stage1.phone_4                AS phone_4,
  sms_type1_stage1.phone_5                AS phone_5,
  sms_type1_stage1.phone_6                AS phone_6,
  threads.Phone                           AS phone_7,
  coalesce(
      sms_type1_stage1.phone_0,
      sms_type1_stage1.phone_1,
      sms_type1_stage1.phone_2,
      sms_type1_stage1.phone_3,
      sms_type1_stage1.phone_4,
      sms_type1_stage1.phone_5,
      sms_type1_stage1.phone_6,
      threads.Phone
  )                                       AS Phone

FROM threads AS threads, sms_type1_stage0 AS sms_type1_stage0, sms_type1_stage1 AS "sms_type1_stage1"
WHERE threads.thread_id = sms_type1_stage1.thread_id AND sms_type1_stage0.record_offset = sms_type1_stage1.record_offset;

DROP VIEW IF EXISTS process_sms_type1_stage1;

CREATE VIEW process_sms_type1_stage1 AS
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
    WHEN phone_1 IS NULL OR phone_2 IS NULL THEN 'outgoing (unknown)'
    ELSE 'incoming (unknown)'
  END)                   AS sent_recieved_text,
  NULL                   AS sent_recieved_hex,
  Phone


FROM process_sms_type1_stage0;


DROP TABLE IF EXISTS process_sms_type1_final;

CREATE TABLE process_sms_type1_final
(
  message_id          INTEGER,
  thread_id           INTEGER,
  timestamp0          TEXT,
  timestamp1          TEXT,
  timestamp2          TEXT,
  timestamp3          TEXT,
  direction           TEXT,
  "direction (hex)"   BLOB,
  Phone               TEXT,
  message             TEXT
);

INSERT INTO process_sms_type1_final
  SELECT

    message_id                                 AS message_id,
    thread_id                                  AS thread_id,

    filetime(FILETIME_0)      AS timestamp0,
    filetime(FILETIME_1)      AS timestamp1,
    filetime(FILETIME_2)      AS timestamp2,
    filetime(FILETIME_3)      AS timestamp3,
    sent_recieved_text                         AS direction,
    hex(sent_recieved_hex)                     AS "direction (hex)",
    Phone                                      AS Phone,
    message                                    AS message
  FROM process_sms_type1_stage1
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

  GROUP BY message_id;


DROP VIEW IF EXISTS type1_messages;

DROP VIEW IF EXISTS process_sms_type1_stage0;
DROP VIEW IF EXISTS process_sms_type1_stage1;

CREATE VIEW type1_messages AS
SELECT DISTINCT
  min(a.message_id, b.message_id,       '<not parsed>')    AS message_id,
  coalesce(a.Phone, b.Phone,            '<not parsed>')    AS Phone,
  coalesce(a.timestamp2, b.timestamp2,  '<not parsed>')    AS timestamp,
  coalesce(a.direction, b.direction,    '<not parsed>')    AS status,
  coalesce(a.message, b.message,        '<not parsed>')    AS message


FROM process_sms_type1_final as a, process_sms_type1_final as b
WHERE a.timestamp2 = b.timestamp2 and a.message_id = b.message_id
GROUP BY a.message_id, b.message, coalesce(a.message_id,b.message_id)
ORDER BY a.message_id DESC;
