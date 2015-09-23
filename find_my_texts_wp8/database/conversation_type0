DROP VIEW IF EXISTS threads;

CREATE VIEW threads as
  SELECT  DISTINCT thread_id as "thread_id", phone as "Phone"
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
    UNION
    SELECT  thread_id, phone_0 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_1 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_2 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_3 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_4 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_5 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_6 as phone
    FROM    sms_type1_stage1
    UNION
    SELECT  thread_id, phone_7 as phone
    FROM    sms_type1_stage1
  )
  WHERE phone NOT NULL;
