# Flask Gemini Chatbot (split files)

A minimal Flask chatbot that uses the Google Gemini API via the official `google-genai` Python SDK. This project demonstrates a small, production-ready layout with separate entrypoints for development and deployment.

---

## Features

* Simple web UI (single-page) for chatting with Gemini.
* Uses the `google-genai` SDK to call the model and generate responses.
* Session-backed short history for simple conversational context.
* Ready for local development and deployment (Render/Gunicorn).

---

## Requirements

* Python 3.10+ (the repo currently tested on 3.11/3.12+)
* `pip` and virtualenv (recommended)
* A Gemini API key (set as `GEMINI_API_KEY` — see below)

---

## Quick start (local)

1. Clone the repo:

```bash
git clone https://github.com/Abhishek100402/help-bot.git
cd help-bot
```

2. Create & activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate     # Windows (PowerShell/CMD)
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Provide environment variables (create a `.env` file or export them):

```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=change-this-secret-for-prod
```

5. Run locally:

```bash
python run.py
# open http://127.0.0.1:5000
```

---

## Production / Render

This repo is ready to deploy to Render (or any host that runs Gunicorn).

**Procfile** (example already included):

```
web: gunicorn wsgi:app
```

If you prefer to directly expose the `app` instance from `app.py` then you can use `gunicorn app:app`, but the recommended, robust approach is to include a `wsgi.py` that imports either an `app` instance or calls `create_app()` if present. That avoids the common `Failed to find attribute 'app' in 'app'` error.

To run locally with Gunicorn for testing:

```bash
gunicorn wsgi:app
```

---

## Environment variables

* `GEMINI_API_KEY` — your Google Gemini API key (required).
* `FLASK_SECRET_KEY` — secret for Flask sessions (recommended to set in production).
* `PORT`, `HOST` — optional overrides for `run.py`.

---

## Files of interest

* `app.py` — main Flask application logic and routes.
* `run.py` — development entrypoint (calls `create_app()` or starts `app.run()` locally).
* `wsgi.py` — recommended WSGI entrypoint for production (used by Gunicorn).
* `Procfile` — instructs hosts (Render/Heroku) how to start the app.
* `requirements.txt` — Python dependencies (include `gunicorn`).

---

## Troubleshooting

* **`Failed to find attribute 'app' in 'app'`**: ensure your Procfile points to a module that exposes a global `app` object (e.g. `web: gunicorn app:app`) or use `wsgi:app` and ensure `wsgi.py` constructs `app` on import.
* **Procfile location**: `Procfile` must live at the repository root.
* **Case-sensitivity**: filenames on Linux are case-sensitive.

---

## Live site

Deployed example: [https://help-bot-5gfo.onrender.com](https://help-bot-5gfo.onrender.com)

---

## License & contact

MIT — feel free to open issues or PRs on the repository.

---
