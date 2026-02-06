START TRANSACTION;

-- Ruoli (upsert compatibile)
START TRANSACTION;

INSERT INTO ruolo (nome, descrizione) VALUES
  ('SYSTEM_ADMIN', 'Amministratore globale del sistema'),
  ('STAFF',        'Staff operativo'),
  ('TUTOR',        'Tutor/Insegnante'),
  ('READER',       'Utente che puo solo visualizzare')
ON DUPLICATE KEY UPDATE
  descrizione = VALUES(descrizione);


-- Permessi (upsert compatibile)
INSERT INTO permesso (codice, descrizione) VALUES
  -- utenti
  ('USER_READ',    'Leggere utenti'),
  ('USER_CREATE',  'Creare utenti'),
  ('USER_UPDATE',  'Modificare utenti'),
  ('USER_DISABLE', 'Disattivare utenti'),

  -- ruoli/permessi
  ('RBAC_READ',    'Leggere ruoli e permessi'),
  ('RBAC_UPDATE',  'Gestire ruoli e permessi'),

  -- didattica
  ('SUBJECT_READ',   'Leggere materie'),
  ('SUBJECT_CREATE', 'Creare materie'),
  ('SUBJECT_UPDATE', 'Modificare materie'),
  ('TOPIC_READ',     'Leggere argomenti'),
  ('TOPIC_UPDATE',   'Gestire argomenti'),
  ('TUTOR_SUBJECT_SET', 'Impostare materie e tariffe tutor'),

  -- lezioni
  ('LESSON_READ',     'Leggere lezioni'),
  ('LESSON_CREATE',   'Creare lezioni'),
  ('LESSON_UPDATE',   'Modificare lezioni'),
  ('LESSON_CANCEL',   'Annullare lezioni'),

  -- pagamenti
  ('PAYMENT_READ',    'Leggere pagamenti'),
  ('PAYMENT_CREATE',  'Creare pagamenti'),
  ('PAYMENT_UPDATE',  'Aggiornare stato pagamenti'),

  -- note
  ('NOTE_READ',    'Leggere note'),
  ('NOTE_CREATE',  'Creare note'),
  ('NOTE_UPDATE',  'Modificare note')
ON DUPLICATE KEY UPDATE
  descrizione = VALUES(descrizione);

INSERT IGNORE INTO ruolo_permesso(ruolo_id,permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'READER'
  AND p.codice IN (
    'USER_READ',
    'SUBJECT_READ','TOPIC_READ',
    'LESSON_READ',
    'PAYMENT_READ','NOTE_READ'
  );

INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'SYSTEM_ADMIN';

INSERT IGNORE INTO ruolo_permesso (ruolo_id, permesso_id)
SELECT r.id, p.id
FROM ruolo r
JOIN permesso p
WHERE r.nome = 'STAFF'
  AND p.codice IN (
    'USER_READ',
    'SUBJECT_READ','TOPIC_READ',
    'LESSON_READ','LESSON_CREATE','LESSON_UPDATE',
    'LESSON_CANCEL','LESSON_CONFIRM',
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
    'LESSON_READ','LESSON_UPDATE',
    'LESSON_CONFIRM','LESSON_MARK_DONE',
    'LESSON_CREATE',
    'PAYMENT_READ',
    'NOTE_READ','NOTE_CREATE'
  );

-- Utente superadmin (evita errore se già esiste id=1 o email unica)
INSERT INTO utente
  (id, username, email, password_hash, nome, cognome, cf, telefono, data_nascita,
   citta, indirizzo, cap, paese, attivo, last_login_at, created_at, updated_at)
VALUES
  (1, 'su_admin', 'su_admin@gmail.com',
   '$argon2id$v=19$m=65536,t=3,p=4$AhfjYGrEFDqBcGDMhpbeug$Boi8+nPfKLGxt9076kop/7QdxAIUJiMxXT2UWrd3uLM',
   'su_admin', 'su_admin', NULL, NULL, NULL,
   NULL, NULL, NULL, NULL, 1,
   '2026-01-15 15:13:00', '2026-01-15 11:32:49', '2026-01-15 16:13:00'
  )
ON DUPLICATE KEY UPDATE
  username = VALUES(username),
  email = VALUES(email),
  password_hash = VALUES(password_hash),
  nome = VALUES(nome),
  cognome = VALUES(cognome),
  attivo = VALUES(attivo),
  last_login_at = VALUES(last_login_at),
  updated_at = VALUES(updated_at);

-- Assegna ruoli a su_admin SENZA hardcodare gli id (robusto)
INSERT IGNORE INTO utente_ruolo (utente_id, ruolo_id, assegnato_at)
SELECT 1, r.id, '2026-01-15 11:33:07'
FROM ruolo r
WHERE r.nome = 'SYSTEM_ADMIN';

INSERT IGNORE INTO utente_ruolo (utente_id, ruolo_id, assegnato_at)
SELECT 1, r.id, '2026-01-15 13:19:00'
FROM ruolo r
WHERE r.nome = 'TUTOR';

INSERT INTO materia (nome, descrizione) VALUES
('ITALIANO', 'Studio della lingua italiana, grammatica, lettura e produzione di testi.'),
('MATEMATICA', 'Aritmetica, algebra, geometria, funzioni e logica matematica.'),
('STORIA', 'Studio degli eventi storici dalle origini alle epoche moderne.'),
('GEOGRAFIA', 'Studio del territorio, delle nazioni, dei climi e delle società umane.'),
('SCIENZE', 'Biologia, chimica, fisica di base e scienze naturali.'),
('INGLESE', 'Lingua inglese: grammatica, lessico, comprensione e produzione.'),
('ARTE E IMMAGINE', 'Disegno, pittura, analisi delle opere d’arte e linguaggi visivi.'),
('MUSICA', 'Teoria musicale, ascolto attivo e pratica musicale di base.'),
('EDUCAZIONE FISICA', 'Attività motoria, sport, salute e cultura del movimento.'),
('TECNOLOGIA', 'Sistemi tecnologici, strumenti digitali e problem-solving tecnico.'),
('INFORMATICA', 'Basi del computer, software, internet, algoritmica introduttiva.'),
('RELIGIONE', 'Studio delle religioni, etica, cultura religiosa.');

COMMIT;