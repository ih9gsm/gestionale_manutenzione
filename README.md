# gestionale_manutenzione

Questa è una semplice webapp Flask per la gestione di segnalazioni, ODS, utenti e preventivi.

## Requisiti

- Python 3.10 o superiore
- Le dipendenze elencate in `requirements.txt`

## Installazione

```bash
pip install -r requirements.txt
```

## Avvio dell'applicazione

```bash
python app.py
```

L'applicazione è configurata per utilizzare un database SQLite `app.db`.

## Funzionalità principali

- Gestione CRUD di segnalazioni e ODS
- Gestione utenti e preventivi
- Generazione di PDF tramite `reportlab`
- Invio di email con allegati tramite SMTP

Questo progetto è un prototipo dimostrativo e non deve essere utilizzato in produzione senza opportune verifiche.

