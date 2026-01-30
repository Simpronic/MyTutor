🇮🇹
# Strumento di Gestione Studenti e Contabilità

## Panoramica

Questo progetto nasce dalla necessità di disporre di un **piccolo tool leggero e personalizzabile** per la gestione degli studenti e della relativa contabilità.

L’obiettivo è fornire una **soluzione gratuita e auto-ospitabile**, focalizzata esclusivamente sulle **funzionalità essenziali**, evitando complessità superflue ma mantenendo la flessibilità necessaria per adattarsi a contesti diversi.

Il software può essere scaricato e utilizzato installandolo su un **proprio server**, garantendo il pieno controllo dei dati e dell’infrastruttura.

---

## Funzionalità

- Gestione di base degli studenti
- Contabilità semplice e tracciamento dei pagamenti legati agli studenti
- Elevata possibilità di personalizzazione
- Soluzione gratuita e self-hosted

---

## Dipendenze e ambiente

- **Python**: 3.10+ (consigliato per FastAPI e dipendenze attuali)
- **Backend**: vedi `requirements.txt`
  - fastapi
  - uvicorn
  - sqlalchemy
  - pymysql
  - argon2-cffi
  - python-jose[cryptography]
  - pydantic[email]
- **Frontend**: HTML/CSS/JS statico (nessun build tool richiesto)

---

## Personalizzazione e Modifica

Il software è **liberamente modificabile** in base alle proprie esigenze.  
È possibile adattarlo, estenderlo o integrarlo nei propri flussi di lavoro senza limitazioni tecniche.

---

## Licenza e Attribuzione

Il progetto è distribuito con una **licenza permissiva**.

È consentito:
- utilizzare il software
- modificarlo
- ridistribuirlo, anche a fini commerciali

L’unico requisito richiesto è la **citazione dell’autore originale**.

---

## Dichiarazione di responsabilità

Il software è fornito “così com’è”, senza alcuna garanzia.  
L’utilizzo è a proprio rischio.


🇬🇧 
# Student Management & Accounting Tool

## Overview

This project was created to address the need for a **small, lightweight, and customizable tool** for managing students and their related accounting data.

The goal is to provide a **free and self-hosted solution** that focuses only on **essential features**, avoiding unnecessary complexity while remaining flexible enough to adapt to different use cases.

The software can be downloaded and deployed on your **own server**, giving users full control over their data and infrastructure.

---

## Features

- Basic student management
- Simple accounting and tracking of student-related payments
- Customizable to fit specific needs
- Self-hosted and free to use

---

## Dependencies & environment

- **Python**: 3.10+ (recommended for FastAPI and current dependencies)
- **Backend**: see `requirements.txt`
  - fastapi
  - uvicorn
  - sqlalchemy
  - pymysql
  - argon2-cffi
  - python-jose[cryptography]
  - pydantic[email]
- **Frontend**: static HTML/CSS/JS (no build tool required)

---

## Customization & Modification

The software is **freely modifiable** according to your own requirements.  
You are encouraged to adapt, extend, or integrate it into your existing workflows.

---

## License & Attribution

This project is released under a permissive license.

You are free to:
- Use the software
- Modify it
- Redistribute it, including for commercial purposes

The **only requirement** is that proper **attribution to the original author** is maintained.

---

## Disclaimer

This software is provided "as is", without warranty of any kind.  
Use it at your own risk.

@@ -114,26 +144,26 @@ For the backend part you can use the VSCode debugger using this configuration:
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload"
            ],
            "jinja": true
        }
    ]
}

running it from the backend folder

## Frontend debugging (VSCode)

Per il frontend puoi usare il debugger JavaScript integrato in VSCode con il browser:

1. Avvia un server statico dalla cartella `frontend`, per esempio:

   ```bash
   cd frontend
   python -m http.server 8000
   ```

2. Aggiungi una voce `launch.json` come questa:

   ```json
   {
     "name": "Debug Frontend (Chrome)",
     "type": "pwa-chrome",
     "request": "launch",
     "url": "http://localhost:8000/html/settings.html",
     "webRoot": "${workspaceFolder}/frontend"
   }
   ```

3. Imposta i breakpoint nei file `frontend/js` e avvia il debugger.