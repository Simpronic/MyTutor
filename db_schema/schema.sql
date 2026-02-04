-- =========================================
-- MyTutor - Schema DB (MySQL 8+)
-- =========================================

SET FOREIGN_KEY_CHECKS = 0;

SET FOREIGN_KEY_CHECKS = 1;

START TRANSACTION;

-- =========================
-- ANAGRAFICA / AUTH
-- =========================
CREATE TABLE paese (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  iso2 CHAR(2) NOT NULL,          -- es: IT, FR, US (ISO 3166-1 alpha-2)
  iso3 CHAR(3) NULL,              -- opzionale (AFG, ITA...), utile per alcune API/dati
  iso_numeric CHAR(3) NULL,       -- opzionale (004, 380...), se ti serve
  attivo TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_paese_iso2 (iso2),
  UNIQUE KEY uq_paese_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE utente (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  email VARCHAR(254) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nome VARCHAR(100) NOT NULL,
  cognome VARCHAR(100) NOT NULL,
  cf CHAR(16) NULL,
  telefono VARCHAR(30) NULL,
  data_nascita DATE NULL,
  iban VARCHAR(50) NULL,
  citta VARCHAR(120) NULL,
  indirizzo VARCHAR(255) NULL,
  cap VARCHAR(10) NULL,
  paese CHAR(2) NULL,

  attivo TINYINT(1) NOT NULL DEFAULT 1,
  last_login_at DATETIME NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_utente_username (username),
  UNIQUE KEY uq_utente_email (email),
  UNIQUE KEY uq_utente_cf (cf),
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
  codice VARCHAR(50) NOT NULL,
  descrizione VARCHAR(255) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_permesso_codice (codice)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE utente_ruolo (
  utente_id BIGINT UNSIGNED NOT NULL,
  ruolo_id SMALLINT UNSIGNED NOT NULL,
  assegnato_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (utente_id, ruolo_id),
  KEY idx_ur_ruolo (ruolo_id),
  CONSTRAINT fk_ur_utente FOREIGN KEY (utente_id)
    REFERENCES utente(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_ur_ruolo FOREIGN KEY (ruolo_id)
    REFERENCES ruolo(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ruolo_permesso (
  ruolo_id SMALLINT UNSIGNED NOT NULL,
  permesso_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (ruolo_id, permesso_id),
  KEY idx_rp_permesso (permesso_id),
  CONSTRAINT fk_rp_ruolo FOREIGN KEY (ruolo_id)
    REFERENCES ruolo(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_rp_permesso FOREIGN KEY (permesso_id)
    REFERENCES permesso(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================
-- DIDATTICA
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
  KEY idx_ma_argomento (argomento_id),
  CONSTRAINT fk_ma_materia FOREIGN KEY (materia_id)
    REFERENCES materia(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_ma_argomento FOREIGN KEY (argomento_id)
    REFERENCES argomento(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tutor_materia (
  tutor_id BIGINT UNSIGNED NOT NULL,
  materia_id BIGINT UNSIGNED NOT NULL,
  prezzo_orario DECIMAL(10,2) NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',
  PRIMARY KEY (tutor_id, materia_id),
  KEY idx_tm_materia (materia_id),
  CONSTRAINT fk_tm_tutor FOREIGN KEY (tutor_id)
    REFERENCES utente(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_tm_materia FOREIGN KEY (materia_id)
    REFERENCES materia(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table sessione(
	token varchar(128),
    utente_id bigint UNSIGNED,
    created_at datetime,
    last_seen_at datetime,
    expires_at datetime,
    
    PRIMARY KEY(token),
    CONSTRAINT uq_sessione_utente_id UNIQUE (utente_id),
    CONSTRAINT fk_sessione_utente FOREIGN KEY(utente_id) REFERENCES utente(id) 
	  ON DELETE CASCADE
    ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- DISPONIBILITÀ
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
  KEY idx_disp_giorno (giorno_settimana),
  CONSTRAINT fk_disp_tutor FOREIGN KEY (tutor_id)
    REFERENCES utente(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================
-- STUDENTI (DUPLICABILI PER TUTOR)
-- =========================
CREATE TABLE studente (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  tutor_id BIGINT UNSIGNED NOT NULL, -- ogni "studente" appartiene a 1 tutor (vincolo richiesto)

  nome VARCHAR(100) NOT NULL,
  cognome VARCHAR(100) NOT NULL,

  email VARCHAR(254) NULL,
  telefono VARCHAR(30) NULL,
  cf CHAR(16) NULL,
  data_nascita DATE NULL,

  citta VARCHAR(120) NULL,
  indirizzo VARCHAR(255) NULL,
  cap VARCHAR(10) NULL,
  paese CHAR(2) NULL,

  attivo TINYINT(1) NOT NULL DEFAULT 1,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),

  KEY idx_studente_tutor (tutor_id),
  KEY idx_studente_cognome_nome (cognome, nome),

  -- Questi due UNIQUE evitano duplicati "dentro lo stesso tutor",
  -- ma permettono duplicazione tra tutor diversi.
  UNIQUE KEY uq_studente_tutor_email (tutor_id, email),
  UNIQUE KEY uq_studente_tutor_cf (tutor_id, cf),

  CONSTRAINT fk_studente_tutor FOREIGN KEY (tutor_id)
    REFERENCES utente(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================
-- LEZIONI
-- =========================
CREATE TABLE lezione (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  tutor_id BIGINT UNSIGNED NOT NULL,

  materia_id BIGINT UNSIGNED NOT NULL,
  argomento_id BIGINT UNSIGNED NULL,

  data_inizio DATETIME NOT NULL,
  data_fine DATETIME NOT NULL,
  timezone VARCHAR(50) NOT NULL DEFAULT 'Europe/Rome',

  stato ENUM('prenotata','confermata','svolta','annullata','no_show')
    NOT NULL DEFAULT 'prenotata',

  prezzo DECIMAL(10,2) NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',

  note TEXT NULL,
  note_private TEXT NULL,
  luogo ENUM('remoto','presenza') NOT NULL DEFAULT 'remoto',

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),

  KEY idx_lezione_tutor_data (tutor_id, data_inizio),
  KEY idx_lezione_materia (materia_id),
  KEY idx_lezione_stato (stato),

  CONSTRAINT fk_lezione_tutor FOREIGN KEY (tutor_id)
    REFERENCES utente(id)
    ON DELETE RESTRICT,

  CONSTRAINT fk_lezione_materia FOREIGN KEY (materia_id)
    REFERENCES materia(id)
    ON DELETE RESTRICT,

  CONSTRAINT fk_lezione_argomento FOREIGN KEY (argomento_id)
    REFERENCES argomento(id)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Partecipanti: una lezione può avere N studenti (min 1 gestito in app o con trigger)
CREATE TABLE lezione_partecipante (
  lezione_id BIGINT UNSIGNED NOT NULL,
  studente_id BIGINT UNSIGNED NOT NULL,

  presenza ENUM('previsto','presente','assente','no_show') NOT NULL DEFAULT 'previsto',
  note TEXT NULL,

  PRIMARY KEY (lezione_id, studente_id),
  KEY idx_lp_studente (studente_id),

  CONSTRAINT fk_lp_lezione FOREIGN KEY (lezione_id)
    REFERENCES lezione(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_lp_studente FOREIGN KEY (studente_id)
    REFERENCES studente(id)
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE lezione_stato_storia (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  lezione_id BIGINT UNSIGNED NOT NULL,
  da_stato ENUM('prenotata','confermata','svolta','annullata','no_show') NULL,
  a_stato  ENUM('prenotata','confermata','svolta','annullata','no_show') NOT NULL,
  cambiato_da BIGINT UNSIGNED NULL,
  cambiato_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  motivo VARCHAR(255) NULL,
  PRIMARY KEY (id),
  KEY idx_lss_lezione (lezione_id),
  KEY idx_lss_cambiato_da (cambiato_da),
  CONSTRAINT fk_lss_lezione FOREIGN KEY (lezione_id)
    REFERENCES lezione(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_lss_cambiato_da FOREIGN KEY (cambiato_da)
    REFERENCES utente(id)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================
-- PAGAMENTI
-- =========================
CREATE TABLE pagamento (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  lezione_id BIGINT UNSIGNED NULL,

  -- MODIFICA: ora punta a studente(id) e non più a utente(id)
  studente_id BIGINT UNSIGNED NOT NULL,

  tutor_id BIGINT UNSIGNED NULL,

  importo DECIMAL(10,2) NOT NULL,
  valuta CHAR(3) NOT NULL DEFAULT 'EUR',

  metodo ENUM('contanti','bonifico','carta','paypal','altro')
    NOT NULL DEFAULT 'altro',
  stato ENUM('creato','autorizzato','pagato','rimborsato','fallito','annullato')
    NOT NULL DEFAULT 'creato',

  riferimento_esterno VARCHAR(255) NULL,
  note TEXT NULL,

  pagato_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),

  KEY idx_pag_lezione (lezione_id),
  KEY idx_pag_studente (studente_id),
  KEY idx_pag_tutor (tutor_id),
  KEY idx_pag_stato (stato),
  KEY idx_pag_tutor_studente (tutor_id, studente_id),

  CONSTRAINT fk_pag_lezione FOREIGN KEY (lezione_id)
    REFERENCES lezione(id)
    ON DELETE SET NULL,

  CONSTRAINT fk_pag_studente FOREIGN KEY (studente_id)
    REFERENCES studente(id)
    ON DELETE RESTRICT,

  CONSTRAINT fk_pag_tutor FOREIGN KEY (tutor_id)
    REFERENCES utente(id)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================
-- NOTE
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
  KEY idx_un_creato_da (creato_da),

  CONSTRAINT fk_un_utente FOREIGN KEY (utente_id)
    REFERENCES utente(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_un_creato_da FOREIGN KEY (creato_da)
    REFERENCES utente(id)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;

--==================
--Utility Tables
--==================

CREATE TABLE IF NOT EXISTS event_log (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_name VARCHAR(128) NOT NULL,
  ran_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  note VARCHAR(255) NULL
);

--==================
--Stored Procedures AND events
--==================

DELIMITER //

CREATE EVENT IF NOT EXISTS ev_test_every_second
ON SCHEDULE EVERY 1 SECOND
DO
BEGIN
DELETE from sessione WHERE expires_at < NOW();
  INSERT INTO event_log(event_name, note)
  VALUES ('ev_test_every_second', 'tick');
END//

DELIMITER ;

--======================
--Comandi utili------
--======================

-- SHOW VARIABLES LIKE 'event_scheduler';

-- Se non è su ON 
-- SET GLOBAL event_scheduler = ON;

-- Per rendere persistente questa cosa (Set global) dovremmo cambiare la configurazione MySql