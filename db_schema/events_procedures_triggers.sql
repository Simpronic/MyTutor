--==================
-- Stored Procedures AND events
--==================

DELIMITER //

CREATE EVENT IF NOT EXISTS delete_expired_sessions
ON SCHEDULE EVERY 10 MINUTE
DO
BEGIN
DELETE from sessione WHERE expires_at < NOW();
  INSERT INTO event_log(event_name, note)
  VALUES ('ev_test_every_second', 'tick');
END//

DELIMITER ;

DELIMITER //

CREATE EVENT IF NOT EXISTS delete_old_logs
ON SCHEDULE EVERY 2 Week
DO
BEGIN
DELETE from sessione WHERE expires_at < NOW();
  DELETE FROM event_log WHERE DATEDIFF(Now(),ran_at) > 15;
END//

DELIMITER ;

/* ======================
-- Comandi utili ------
 ======================*/

-- SHOW VARIABLES LIKE 'event_scheduler';

-- Se non è su ON 
-- SET GLOBAL event_scheduler = ON;

-- Per rendere persistente questa cosa (Set global) dovremmo cambiare la configurazione MySql