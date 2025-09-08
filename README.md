# ChatGPT Backend (FastAPI + OpenAI)

Questo progetto fornisce un backend in **Python** basato su **FastAPI** e **Uvicorn** per integrare le API di OpenAI (ChatGPT).

## 🚀 Funzionalità

- Endpoint `/chat` per risposte non-streaming.
- Endpoint `/chat/stream` per risposte in **streaming** (token-by-token, via SSE).
- Gestione degli errori e retry automatici (con backoff esponenziale).
- Schemi dati validati con **Pydantic**.
- Configurazione tramite `.env`.

---

## 📂 Struttura del progetto

```
your-backend/
├─ app/
│  ├─ main.py              # Entrypoint FastAPI
│  ├─ deps.py              # Dipendenze condivise
│  ├─ schemas.py           # Schemi Pydantic (input/output)
│  ├─ openai_client.py     # Inizializzazione client OpenAI
│  ├─ routers/
│  │   ├─ chat.py          # Endpoint per le chat
│  │   └─ tools.py         # Endpoint extra/tool
│  └─ utils/
│      └─ backoff.py       # Retry con backoff esponenziale
├─ tests/
│  └─ test_chat.py         # Test automatici (pytest)
├─ .env                    # Variabili ambiente (API key)
├─ pyproject.toml / requirements.txt
└─ README.md
```

---

## ⚙️ Installazione

1. Clona il progetto:

   ```bash
   git clone https://github.com/tuo-user/chatgpt-backend.git
   cd chatgpt-backend
   ```

2. Crea un ambiente virtuale e attivalo:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura la tua chiave API in `.env`:
   ```env
   OPENAI_API_KEY=sk-xxxxx
   ```

---

## ▶️ Avvio dell'applicazione

In fase di sviluppo (con auto-reload):

```bash
python3 -m uvicorn app.main:app --reload --port 8000
# oppure
uvicorn app.main:app --reload --port 8000
```

Poi apri:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → Swagger UI
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) → Documentazione alternativa

---

## 🧪 Test

Per eseguire i test (con `pytest`):

```bash
pytest
```

---

## 📦 Produzione

In produzione si consiglia di usare **Gunicorn + Uvicorn workers**:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 📜 Licenza

MIT License
