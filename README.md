# Chatting Bot — Stateful Multi-Turn Chat API

A multi-user chat API where conversations persist and the **memory layer** decides
what context actually reaches the model when a conversation outgrows the window.
The chat loop is trivial; the engineering is memory management, persistence, and
a real evaluation harness.

## Stack
FastAPI · async SQLAlchemy · SQLite · JWT auth · pluggable LLM provider

## Data model
`User` → `Conversation` → `Message`
Key columns on `Message`: `token_count` (size measured once, at write time) and
`is_summarized` (still live vs. already folded into a summary). Those two are what
make this a memory system, not a chat wrapper.

## The core idea
A **memory strategy** is one function:
> given the live messages + a token budget (+ optional summary) → the list of
> messages to actually send to the model.

Every approach is an implementation of that interface (`app/memory/base.py`).

## Build phases
- **v1 (done / runnable):** auth, persistence, buffer memory, LLM call loop.
  Runs fully offline with the `echo` provider — no API key needed.
- **v2 (you write):** `window.py`, `summary.py` — handle overflow.
- **v3 (you write):** `vector.py` + `eval/harness.py` — retrieval + measured comparison.

## What's stubbed for you
`memory/window.py`, `memory/summary.py`, `memory/vector.py`, `eval/harness.py`
each raise `NotImplementedError` with a spec in the docstring.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # defaults run offline (echo provider)
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Quick smoke test (in /docs)
1. `POST /auth/register` → copy the token, click **Authorize**.
2. `POST /conversations` → note the `id`.
3. `POST /chat/{id}` a few times → echo provider replies, messages persist.
4. Restart the server, `GET /conversations/{id}/messages` → history survived.
