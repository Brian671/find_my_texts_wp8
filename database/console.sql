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
DROP VIEW IF EXISTS threads;

CREATE VIEW threads as
SELECT  DISTINCT thread_id as "Thread_ID", phone as "Phone"
FROM (
  SELECT  thread_id, phone_0 as phone
  FROM    sms_type0_stage1 as sms_type0_stage1
  UNION
  SELECT  thread_id, phone_1 as phone
  FROM    sms_type0_stage1 as sms_type0_stage1
  UNION
  SELECT  thread_id, phone_2 as phone
  FROM    sms_type0_stage1 as sms_type0_stage1
  UNION
  SELECT  thread_id, phone_3 as phone
  FROM    sms_type0_stage1 as sms_type0_stage1
  UNION
  SELECT  thread_id, phone_0 as phone
  FROM    conversation_type0_stage1
  UNION
  SELECT  thread_id, phone_1 as phone
  FROM    conversation_type0_stage1
  UNION
  SELECT  thread_id, phone_2 as phone
  FROM    conversation_type0_stage1
)
WHERE phone NOT NULL;

DROP VIEW IF EXISTS message_intermediate;

CREATE VIEW message_intermediate AS
SELECT DISTINCT
message_id                                                  AS message_id,
sms_type0_stage1.thread_id                                  AS thread_id,
NULLIF(printf('%s.%-07d',
              strftime('%d-%m-%Y %H:%M:%S',
                       ((FILETIME_0 - 116444736000000000) / 10000000),
                       'unixepoch',
                       'localtime'),
              FILETIME_0 % 10000000), '.0000000')
                                                            AS timestamp0,
NULLIF(printf('%s.%-07d',
              strftime('%d-%m-%Y %H:%M:%S',
                       ((FILETIME_1 - 116444736000000000) / 10000000),
                       'unixepoch',
                       'localtime'),
              FILETIME_1 % 10000000), '.0000000')
                                                            AS timestamp1,
NULLIF(printf('%s.%-07d',
              strftime('%d-%m-%Y %H:%M:%S',
                       ((coalesce(FILETIME_2, FILETIME_2b) - 116444736000000000) / 10000000),
                       'unixepoch',
                       'localtime'),
              FILETIME_2b % 10000000), '.0000000')
                                                            AS timestamp2,
NULLIF(printf('%s.%-07d',
              strftime('%d-%m-%Y %H:%M:%S',
                       ((FILETIME_3 - 116444736000000000) / 10000000),
                       'unixepoch',
                       'localtime'),
              FILETIME_3 % 10000000), '.0000000')
                                                            AS timestamp3,
direction                                                   AS direction,
coalesce(phone_0, phone_1, phone_2, phone_3, threads.Phone) AS Phone,
message                                                     AS message,
sms_type0_stage1.FILETIME_3                                 AS f3,
coalesce(sms_type0_stage1.FILETIME_2,
         sms_type0_stage1.FILETIME_2b)                      AS f2,
sms_type0_stage1.FILETIME_1                                 AS f1,
sms_type0_stage1.FILETIME_0                                 AS f0
FROM
(
    sms_type0_stage1
    INNER JOIN threads
      ON sms_type0_stage1.thread_id = threads.Thread_ID
)

WHERE
sms_type0_stage1.message_id IS NOT NULL OR
sms_type0_stage1.thread_id IS NOT NULL OR
sms_type0_stage1.content IS NOT NULL OR
sms_type0_stage1.message IS NOT NULL OR
sms_type0_stage1.FILETIME_0 IS NOT NULL OR
sms_type0_stage1.FILETIME_1 IS NOT NULL OR
sms_type0_stage1.FILETIME_2 IS NOT NULL OR
sms_type0_stage1.FILETIME_3 IS NOT NULL OR
sms_type0_stage1.direction IS NOT NULL OR
sms_type0_stage1.phone_0 IS NOT NULL OR
sms_type0_stage1.phone_1 IS NOT NULL OR
sms_type0_stage1.phone_2 IS NOT NULL OR
sms_type0_stage1.phone_3 IS NOT NULL

GROUP BY record_offset
ORDER BY message_id DESC;

DROP VIEW IF EXISTS messages;

CREATE VIEW messages AS
SELECT min(a.message_id, b.message_id)    AS message_id,
  coalesce(a.timestamp3, b.timestamp3)    AS "sent/recieved",
  min(a.thread_id, b.thread_id)           AS thread_id,
  coalesce(a.message, b.message)          AS message
FROM message_intermediate as a, message_intermediate as b
WHERE a.timestamp3 = b.timestamp3 or a.message_id = b.message_id
GROUP BY coalesce(a.timestamp0, b.timestamp0), coalesce(a.message_id,b.message_id)
ORDER BY a.message_id;
