
DROP VIEW IF EXISTS type_1_with_bin;
CREATE VIEW type_1_with_bin AS
  SELECT
    a.phone_0,
    a.phone_1,
    a.phone_2,
    a.phone_3,
    a.message,
    a.message_id,
    a.thread_id,
    a.FILETIME_0,
    a.FILETIME_1,
    a.FILETIME_2,
    a.FILETIME_3,
    b.full_binary
  FROM sms_type1_stage1 as a, sms_type1_full_binaries as b
  WHERE b.record_offset = a.record_offset and
        a.SMStext is NOT NULL or a.FILETIME_0 is not NULL;