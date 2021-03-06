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





DROP VIEW IF EXISTS process_sms_type0_stage0;
CREATE VIEW process_sms_type0_stage0 AS
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

DROP VIEW IF EXISTS process_sms_type0_stage1;

CREATE VIEW process_sms_type0_stage1 AS
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


FROM process_sms_type0_stage0;


DROP TABLE IF EXISTS process_sms_type0_final;
CREATE TABLE process_sms_type0_final
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

INSERT INTO process_sms_type0_final
  (message_id, thread_id, timestamp0, timestamp1, timestamp2, timestamp3, direction, "direction (hex)", Phone, message)

  SELECT

    message_id                AS message_id,
    thread_id                 AS thread_id,

    filetime(FILETIME_0)      AS timestamp0,
    filetime(FILETIME_1)      AS timestamp1,
    filetime(FILETIME_2)      AS timestamp2,
    filetime(FILETIME_3)      AS timestamp3,

    sent_recieved_text        AS direction,
    hex(sent_recieved_hex)    AS "direction (hex)",
    Phone                     AS Phone,
    message                   AS message
  FROM process_sms_type0_stage1
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



SELECT count(message_id) FROM sms_type0_stage1;

SELECT * FROM sms_type0_stage1;

DROP VIEW IF EXISTS type0_messages;


CREATE VIEW type0_messages AS
SELECT DISTINCT
  min(a.message_id, b.message_id,       '<not parsed>')    AS message_id,
  coalesce(a.Phone, b.Phone,            '<not parsed>')    AS Phone,
  coalesce(a.timestamp3, b.timestamp3,  '<not parsed>')    AS timestamp,
  coalesce(a.direction, b.direction,    '<not parsed>')    AS status,
  coalesce(a.message, b.message,        '<not parsed>')    AS message


FROM process_sms_type0_final as a, process_sms_type0_final as b
WHERE a.timestamp2 = b.timestamp2 and a.message_id = b.message_id
GROUP BY a.message_id, b.message, coalesce(a.message_id,b.message_id)
ORDER BY a.message_id DESC;
