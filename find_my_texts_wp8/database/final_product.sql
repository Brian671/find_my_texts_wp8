
DROP VIEW IF EXISTS create_union;

CREATE VIEW create_union AS
  SELECT DISTINCT *
  FROM
    (
      SELECT *
      FROM type0_messages
      UNION
      SELECT *
      FROM type1_messages
    )
ORDER BY message_id DESC;


DROP VIEW IF EXISTS all_read;

CREATE VIEW all_read AS
  SELECT *
  FROM create_union
  WHERE status=='incoming (read)';


DROP VIEW IF EXISTS all_unread;

CREATE VIEW all_unread AS
  SELECT *
  FROM create_union
  WHERE status=='incoming (unread)';


DROP VIEW IF EXISTS all_sent;

CREATE VIEW all_sent AS
  SELECT *
  FROM create_union
  WHERE status=='outgoing (sent)';


DROP VIEW IF EXISTS all_draft;

CREATE VIEW all_draft AS
  SELECT *
  FROM create_union
  WHERE status=='outgoing (unknown, possibly draft)';



DROP VIEW IF EXISTS all_incoming_unknown;

CREATE VIEW all_incoming_unknown AS
  SELECT *
  FROM create_union
  WHERE status=='incoming (unknown)';


DROP VIEW IF EXISTS all_outgoing_unknown;

CREATE VIEW all_outgoing_unknown AS
  SELECT *
  FROM create_union
  WHERE status=='outgoing (unknown)';



DROP VIEW IF EXISTS messages;

CREATE VIEW messages AS
  SELECT DISTINCT message_id, timestamp, printf('%s', Phone) as Phone, status, message
  FROM (
    SELECT *
    FROM
      (
        SELECT *
        FROM all_sent
        UNION
        SELECT *
        FROM all_draft
        UNION
        SELECT *
        FROM all_outgoing_unknown
        UNION
        SELECT *
        FROM all_read
        UNION
        SELECT *
        FROM all_unread
        UNION
        SELECT *
        FROM all_incoming_unknown
      )

  )
  GROUP BY message_id
  ORDER BY message_id DESC;


