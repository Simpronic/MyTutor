CREATE OR REPLACE DATABASE MyTutor

-- =========================
-- ANAGRAFICA / AUTH
-- =========================

CREATE TABLE utente (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  email VARCHAR(254) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nome VARCHAR(100) NOT NULL,
  cognome VARCHAR(100) NOT NULL,
  cf VARCHAR(16) NULL,
  telefono VARCHAR(30) NULL,
  data_nascita DATE NULL,

  citta VARCHAR(120) NULL,
  indirizzo VARCHAR(255) NULL,
  cap VARCHAR(10) NULL,
  paese VARCHAR(2) NULL, -- ISO2 (es. IT)

  attivo TINYINT(1) NOT NULL DEFAULT 1,
  last_login_at DATETIME NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_utente_username (username),
  UNIQUE KEY uq_utente_email (email),
  KEY idx_utente_cognome_nome (cognome, nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ruolo (
  id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  descrizione VARCHAR(255) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ruolo_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE permesso (
  id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  codice VARCHAR(50) NOT NULL,          -- es. "LESSON_READ"
  descrizione VARCHAR(255) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_permesso_codice (codice)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE utente_ruolo (
  utente_id BIGINT UNSIGNED NOT NULL,
  ruolo_id SMALLINT UNSIGNED NOT NULL,
  assegnato_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (utente_id, ruolo_id),
  KEY idx_ur_ruolo (ruolo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ruolo_permesso (
  ruolo_id SMALLINT UNSIGNED NOT NULL,
  permesso_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (ruolo_id, permesso_id),
  KEY idx_rp_permesso (permesso_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- ORGANIZZAZIONI / SEDI
-- =========================

CREATE TABLE organizzazione (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(200) NOT NULL,
  piva VARCHAR(20) NULL,
  email VARCHAR(254) NULL,
  telefono VARCHAR(30) NULL,
  note TEXT NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_org_piva (piva),
  KEY idx_org_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sede (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  organizzazione_id BIGINT UNSIGNED NULL, -- FK dopo
  nome VARCHAR(200) NULL,
  citta VARCHAR(120) NULL,
  cap VARCHAR(10) NULL,
  indirizzo VARCHAR(255) NULL,
  note TEXT NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  KEY idx_sede_org (organizzazione_id),
  KEY idx_sede_citta (citta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE organizzazione_utente (
  organizzazione_id BIGINT UNSIGNED NOT NULL,
  utente_id BIGINT UNSIGNED NOT NULL,
  ruolo_in_org VARCHAR(50) NULL, -- es. "tutor", "admin", "staff"
  attivo TINYINT(1) NOT NULL DEFAULT 1,
  associato_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (organizzazione_id, utente_id),
  KEY idx_ou_utente (utente_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- DIDATTICA: MATERIE / ARGOMENTI
-- =========================

CREATE TABLE materia (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(200) NOT NULL,
  descrizione TEXT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_materia_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE argomento (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(200) NOT NULL,
  descrizione TEXT NULL,
  PRIMARY KEY (id),
  KEY idx_argomento_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE materia_argomento (
  materia_id BIGINT UNSIGNED NOT NULL,
  argomento_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (materia_id, argomento_id),
  KEY idx_ma_argomento (argomento_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- quali materie può insegnare un tutor (utente con ruolo "tutor")
CREATE TABLE tutor_materia (
  tutor_id BIGINT UNSIGNED NOT NULL,
  materia_id BIGINT UNSIGNED NOT NULL,
  prezzo_orario DECIMAL(10,2) NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',
  PRIMARY KEY (tutor_id, materia_id),
  KEY idx_tm_materia (materia_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- DISPONIBILITÀ / PRENOTAZIONI / LEZIONI
-- =========================

CREATE TABLE disponibilita_tutor (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  tutor_id BIGINT UNSIGNED NOT NULL,
  giorno_settimana TINYINT UNSIGNED NOT NULL, -- 1=Lun ... 7=Dom
  ora_inizio TIME NOT NULL,
  ora_fine TIME NOT NULL,
  timezone VARCHAR(50) NOT NULL DEFAULT 'Europe/Rome',
  attiva TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_disp_tutor (tutor_id),
  KEY idx_disp_giorno (giorno_settimana)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lezione (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  organizzazione_id BIGINT UNSIGNED NULL,
  sede_id BIGINT UNSIGNED NULL,

  tutor_id BIGINT UNSIGNED NOT NULL,
  studente_id BIGINT UNSIGNED NOT NULL,

  materia_id BIGINT UNSIGNED NOT NULL,
  argomento_id BIGINT UNSIGNED NULL,

  data_inizio DATETIME NOT NULL,
  data_fine DATETIME NOT NULL,
  timezone VARCHAR(50) NOT NULL DEFAULT 'Europe/Rome',

  stato ENUM('prenotata','confermata','svolta','annullata','no_show') NOT NULL DEFAULT 'prenotata',

  prezzo DECIMAL(10,2) NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',

  note TEXT NULL,
  note_private TEXT NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  KEY idx_lezione_tutor_data (tutor_id, data_inizio),
  KEY idx_lezione_studente_data (studente_id, data_inizio),
  KEY idx_lezione_org (organizzazione_id),
  KEY idx_lezione_materia (materia_id),
  KEY idx_lezione_stato (stato)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- storicizza cambi stato (utile per audit)
CREATE TABLE lezione_stato_storia (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  lezione_id BIGINT UNSIGNED NOT NULL,
  da_stato ENUM('prenotata','confermata','svolta','annullata','no_show') NULL,
  a_stato ENUM('prenotata','confermata','svolta','annullata','no_show') NOT NULL,
  cambiato_da BIGINT UNSIGNED NULL, -- utente che ha cambiato (tutor/admin)
  cambiato_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  motivo VARCHAR(255) NULL,
  PRIMARY KEY (id),
  KEY idx_lss_lezione (lezione_id),
  KEY idx_lss_cambiato_da (cambiato_da)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- PAGAMENTI / FATTURAZIONE
-- =========================

CREATE TABLE pagamento (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  lezione_id BIGINT UNSIGNED NULL,
  studente_id BIGINT UNSIGNED NOT NULL,
  tutor_id BIGINT UNSIGNED NULL,

  importo DECIMAL(10,2) NOT NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',

  metodo ENUM('contanti','bonifico','carta','paypal','altro') NOT NULL DEFAULT 'altro',
  stato  ENUM('creato','autorizzato','pagato','rimborsato','fallito','annullato') NOT NULL DEFAULT 'creato',

  riferimento_esterno VARCHAR(255) NULL, -- id transazione gateway
  note TEXT NULL,

  pagato_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  KEY idx_pag_studente (studente_id),
  KEY idx_pag_lezione (lezione_id),
  KEY idx_pag_stato (stato)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- NOTE / DOCUMENTI (opzionale ma utile)
-- =========================

CREATE TABLE utente_note (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  utente_id BIGINT UNSIGNED NOT NULL,
  tipo ENUM('pagamento','profilo','altro') NOT NULL DEFAULT 'altro',
  testo TEXT NOT NULL,
  creato_da BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_un_utente (utente_id),
  KEY idx_un_creato_da (creato_da)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




-- utente_ruolo
ALTER TABLE utente_ruolo
  ADD CONSTRAINT fk_ur_utente FOREIGN KEY (utente_id) REFERENCES utente(id),
  ADD CONSTRAINT fk_ur_ruolo  FOREIGN KEY (ruolo_id)  REFERENCES ruolo(id);

-- ruolo_permesso
ALTER TABLE ruolo_permesso
  ADD CONSTRAINT fk_rp_ruolo    FOREIGN KEY (ruolo_id)    REFERENCES ruolo(id),
  ADD CONSTRAINT fk_rp_permesso FOREIGN KEY (permesso_id) REFERENCES permesso(id);

-- sede -> organizzazione
ALTER TABLE sede
  ADD CONSTRAINT fk_sede_org FOREIGN KEY (organizzazione_id) REFERENCES organizzazione(id);

-- organizzazione_utente
ALTER TABLE organizzazione_utente
  ADD CONSTRAINT fk_ou_org    FOREIGN KEY (organizzazione_id) REFERENCES organizzazione(id),
  ADD CONSTRAINT fk_ou_utente FOREIGN KEY (utente_id)         REFERENCES utente(id);

-- materia_argomento
ALTER TABLE materia_argomento
  ADD CONSTRAINT fk_ma_materia   FOREIGN KEY (materia_id)   REFERENCES materia(id),
  ADD CONSTRAINT fk_ma_argomento FOREIGN KEY (argomento_id) REFERENCES argomento(id);

-- tutor_materia
ALTER TABLE tutor_materia
  ADD CONSTRAINT fk_tm_tutor   FOREIGN KEY (tutor_id)   REFERENCES utente(id),
  ADD CONSTRAINT fk_tm_materia FOREIGN KEY (materia_id) REFERENCES materia(id);

-- disponibilita_tutor
ALTER TABLE disponibilita_tutor
  ADD CONSTRAINT fk_disp_tutor FOREIGN KEY (tutor_id) REFERENCES utente(id);

-- lezione
ALTER TABLE lezione
  ADD CONSTRAINT fk_lezione_org      FOREIGN KEY (organizzazione_id) REFERENCES organizzazione(id),
  ADD CONSTRAINT fk_lezione_sede     FOREIGN KEY (sede_id)           REFERENCES sede(id),
  ADD CONSTRAINT fk_lezione_tutor    FOREIGN KEY (tutor_id)          REFERENCES utente(id),
  ADD CONSTRAINT fk_lezione_studente FOREIGN KEY (studente_id)       REFERENCES utente(id),
  ADD CONSTRAINT fk_lezione_materia  FOREIGN KEY (materia_id)        REFERENCES materia(id),
  ADD CONSTRAINT fk_lezione_argomento FOREIGN KEY (argomento_id)     REFERENCES argomento(id);

-- lezione_stato_storia
ALTER TABLE lezione_stato_storia
  ADD CONSTRAINT fk_lss_lezione    FOREIGN KEY (lezione_id)   REFERENCES lezione(id),
  ADD CONSTRAINT fk_lss_cambiato_da FOREIGN KEY (cambiato_da) REFERENCES utente(id);

-- pagamento
ALTER TABLE pagamento
  ADD CONSTRAINT fk_pag_lezione   FOREIGN KEY (lezione_id)   REFERENCES lezione(id),
  ADD CONSTRAINT fk_pag_studente  FOREIGN KEY (studente_id)  REFERENCES utente(id),
  ADD CONSTRAINT fk_pag_tutor     FOREIGN KEY (tutor_id)     REFERENCES utente(id);

-- utente_note
ALTER TABLE utente_note
  ADD CONSTRAINT fk_un_utente   FOREIGN KEY (utente_id) REFERENCES utente(id),
  ADD CONSTRAINT fk_un_creato_da FOREIGN KEY (creato_da) REFERENCES utente(id);



--Inserimenti base 
START TRANSACTION; 

INSERT INTO ruolo (nome, descrizione) VALUES
  ('SYSTEM_ADMIN', 'Amministratore globale del sistema'),
  ('ORG_ADMIN',    'Amministratore di una specifica organizzazione'),
  ('STAFF',        'Staff operativo (segreteria/gestione)'),
  ('TUTOR',        'Tutor/Insegnante'),
  ('STUDENTE',     'Studente')
ON DUPLICATE KEY UPDATE descrizione = VALUES(descrizione);


INSERT INTO permesso (codice, descrizione) VALUES
  -- utenti
  ('USER_READ',    'Leggere utenti'),
  ('USER_CREATE',  'Creare utenti'),
  ('USER_UPDATE',  'Modificare utenti'),
  ('USER_DISABLE', 'Disattivare utenti'),

  -- ruoli/permessi
  ('RBAC_READ',    'Leggere ruoli e permessi'),
  ('RBAC_UPDATE',  'Gestire ruoli e permessi'),

  -- organizzazioni/sedi
  ('ORG_READ',     'Leggere organizzazioni'),
  ('ORG_CREATE',   'Creare organizzazioni'),
  ('ORG_UPDATE',   'Modificare organizzazioni'),
  ('SEDE_READ',    'Leggere sedi'),
  ('SEDE_UPDATE',  'Gestire sedi'),

  -- didattica (materie/argomenti)
  ('SUBJECT_READ',   'Leggere materie'),
  ('SUBJECT_CREATE', 'Creare materie'),
  ('SUBJECT_UPDATE', 'Modificare materie'),
  ('TOPIC_READ',     'Leggere argomenti'),
  ('TOPIC_UPDATE',   'Gestire argomenti'),
  ('TUTOR_SUBJECT_SET', 'Impostare materie e tariffe tutor'),

  -- disponibilità
  ('AVAIL_READ',   'Leggere disponibilità tutor'),
  ('AVAIL_WRITE',  'Creare/modificare disponibilità tutor'),

  -- lezioni
  ('LESSON_READ',     'Leggere lezioni'),
  ('LESSON_CREATE',   'Creare lezioni (prenotazione)'),
  ('LESSON_UPDATE',   'Modificare lezioni'),
  ('LESSON_CANCEL',   'Annullare lezioni'),
  ('LESSON_CONFIRM',  'Confermare lezioni'),
  ('LESSON_MARK_DONE','Segnare lezione svolta/no_show'),

  -- pagamenti
  ('PAYMENT_READ',    'Leggere pagamenti'),
  ('PAYMENT_CREATE',  'Creare pagamenti'),
  ('PAYMENT_UPDATE',  'Aggiornare stato pagamenti/rimborsi'),

  -- note
  ('NOTE_READ',    'Leggere note'),
  ('NOTE_CREATE',  'Creare note'),
  ('NOTE_UPDATE',  'Modificare note')
ON DUPLICATE KEY UPDATE descrizione = VALUES(descrizione);


INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'SYSTEM_ADMIN';


INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'ORG_ADMIN'
  AND p.codice IN (
    'USER_READ','USER_CREATE','USER_UPDATE','USER_DISABLE',
    'RBAC_READ',
    'ORG_READ','ORG_CREATE','ORG_UPDATE',
    'SEDE_READ','SEDE_UPDATE',
    'SUBJECT_READ','SUBJECT_CREATE','SUBJECT_UPDATE',
    'TOPIC_READ','TOPIC_UPDATE',
    'LESSON_READ','LESSON_CREATE','LESSON_UPDATE','LESSON_CANCEL','LESSON_CONFIRM','LESSON_MARK_DONE',
    'PAYMENT_READ','PAYMENT_CREATE','PAYMENT_UPDATE',
    'NOTE_READ','NOTE_CREATE','NOTE_UPDATE'
  );


INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'STAFF'
  AND p.codice IN (
    'USER_READ',
    'ORG_READ','SEDE_READ',
    'SUBJECT_READ','TOPIC_READ',
    'LESSON_READ','LESSON_CREATE','LESSON_UPDATE','LESSON_CANCEL','LESSON_CONFIRM',
    'PAYMENT_READ','PAYMENT_CREATE',
    'NOTE_READ','NOTE_CREATE'
  );


INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'TUTOR'
  AND p.codice IN (
    'SUBJECT_READ','TOPIC_READ',
    'TUTOR_SUBJECT_SET',
    'AVAIL_READ','AVAIL_WRITE',
    'LESSON_READ','LESSON_UPDATE',      -- poi nel codice limiti alle proprie lezioni
    'LESSON_CONFIRM','LESSON_MARK_DONE',
    'PAYMENT_READ',                     -- spesso solo lettura di incassi propri
    'NOTE_READ','NOTE_CREATE'
  );


INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'STUDENTE'
  AND p.codice IN (
    'SUBJECT_READ','TOPIC_READ',
    'LESSON_READ','LESSON_CREATE','LESSON_CANCEL',  -- limitate alle proprie lezioni
    'PAYMENT_READ','PAYMENT_CREATE',
    'NOTE_READ'
  );
COMMIT;