# Frontend structure

Questa cartella è organizzata per mantenere separati i moduli condivisi, i componenti UI e gli script specifici delle pagine.

## Struttura

- `html/`: pagine HTML e partials.
- `css/`: stili globali e temi.
- `js/`
  - `core/`: moduli condivisi (API, router, gestione sessione).
  - `components/`: componenti riutilizzabili (modali, web components).
  - `pages/`: script legati alle singole pagine.
    - `settings/`: logica specifica delle impostazioni.

## Linee guida rapide

- Evita logica duplicata: se la stessa logica serve a più pagine, spostala in `js/core/` o `js/components/`.
- Mantieni gli script delle pagine leggeri: importa solo ciò che serve.
- Quando aggiungi nuove pagine, inserisci il relativo script in `js/pages/`.