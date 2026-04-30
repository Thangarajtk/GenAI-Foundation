# Day 06 — IT Help Desk Chat App

A full-stack chatbot demonstrating how to connect a **FastAPI backend** to a **vanilla JS frontend** using the OpenAI API with **real-time streaming**.

---

## Architecture

```
Browser (localhost:3000)
    │  fetch POST /chat/stream   (Server-Sent Events)
    ▼
Express static server  ──serves──►  public/index.html
                                         │
                              (fetch to port 8000)
                                         ▼
                              FastAPI backend (localhost:8000)
                                         │
                                    OpenAI API
```

### Folder structure

```
chatapp/
├── backend/
│   ├── main.py            ← FastAPI app (all endpoints)
│   ├── requirements.txt   ← Python dependencies
│   └── .env.example       ← copy to .env and add your key
└── frontend/
    ├── server.js          ← Express static file server
    ├── package.json
    └── public/
        └── index.html     ← Chat UI (pure HTML/CSS/JS)
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat` | Single response (full JSON) |
| `POST` | `/chat/stream` | Streaming response (SSE, token by token) |
| `DELETE` | `/chat/{session_id}` | Clear conversation history |

### How streaming works (SSE)

`POST /chat/stream` returns a `text/event-stream`. Each event is a JSON object:

```
data: {"type": "session_id", "content": "<uuid>"}   ← sent first
data: {"type": "delta",      "content": "Hello"}    ← one per token
data: {"type": "done"}                              ← stream finished
data: {"type": "error",      "content": "..."}      ← on failure
```

The frontend reads these with the `ReadableStream` API and appends each token to the chat bubble in real time.

---

## Setup & Run

### Prerequisites
- Python 3.10+ with a virtual environment
- Node.js 18+
- An OpenAI API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 1 — Configure the API key

```bash
cd Day06/chatapp/backend
cp .env.example .env
# Open .env and replace sk-... with your actual key
```

### Step 2 — Start the backend

Open a terminal and run:

```bash
# From the repo root
source .venv/bin/activate
cd Day06/chatapp/backend
python -m uvicorn main:app --port 8000
```

Expected output:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Verify it's running:
```bash
curl http://localhost:8000/
# → {"status":"ok","service":"Day 06 Chatbot API"}
```

### Step 3 — Start the frontend

Open a **second terminal** and run:

```bash
cd Day06/chatapp/frontend
npm install      # only needed the first time
npm start
```

Expected output:
```
Frontend running at http://localhost:3000
```

### Step 4 — Open the chat UI

Go to **http://localhost:3000** in your browser.

---

## Exercises for Trainees

1. **Change the persona** — Edit `SYSTEM_PROMPT` in `main.py`. Try: HR assistant, onboarding bot, finance helper.
2. **Adjust temperature** — In `main.py`, change `temperature=0.5` to `0.0` (deterministic) or `1.0` (creative). Observe the difference.
3. **Add a message counter** — In `index.html`, display the number of messages sent in the current session.
4. **Limit history length** — In `chat_stream()`, slice history to the last N messages to simulate a sliding context window.
5. **Switch model** — Change `MODEL = "gpt-4.1"` to `"gpt-4o-mini"` for faster/cheaper responses.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `401 Invalid API key` | Check `.env` — make sure the key starts with `sk-` |
| `Address already in use` | Run `fuser -k 8000/tcp` or `fuser -k 3000/tcp` |
| Tokens not streaming | Make sure you're calling `/chat/stream`, not `/chat` |
| CORS error in browser | Confirm the backend is running on port 8000 |
| `npm: command not found` | Install Node.js from [nodejs.org](https://nodejs.org) |
