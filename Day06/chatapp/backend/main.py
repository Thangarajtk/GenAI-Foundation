"""
Day 06 Chat App — FastAPI Backend
===================================
POST /chat  →  send a message, get a reply
GET  /      →  health check

Chat history is kept in memory per session_id.
"""

import json
import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI, AuthenticationError, RateLimitError

load_dotenv()

app = FastAPI(title="Day 06 Help Desk Chatbot")

# Allow the frontend (any origin in dev) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4.1"

SYSTEM_PROMPT = (
    "You are a helpful internal IT Help Desk assistant. "
    "Answer employee questions about software tools, access issues, and company systems. "
    "Be concise, friendly, and professional. "
    "If you don't know the answer, say so and suggest contacting IT directly."
)

# In-memory session store  { session_id: [{"role": ..., "content": ...}] }
sessions: dict[str, list[dict]] = {}


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str = ""          # empty → server creates a new one


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    history: list[dict]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok", "service": "Day 06 Chatbot API"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Resolve or create session
    sid = req.session_id.strip() or str(uuid.uuid4())
    if sid not in sessions:
        sessions[sid] = []

    history = sessions[sid]
    history.append({"role": "user", "content": req.message})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            temperature=0.5,
            max_tokens=512,
        )
        reply = resp.choices[0].message.content.strip()
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid OpenAI API key.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again shortly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    history.append({"role": "assistant", "content": reply})
    return ChatResponse(reply=reply, session_id=sid, history=history)


@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"cleared": session_id}


# ---------------------------------------------------------------------------
# Streaming endpoint
# ---------------------------------------------------------------------------
@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """
    Same as /chat but returns a text/event-stream response.

    Each Server-Sent Event carries one JSON object:
      {"type": "delta",      "content": "<token>"}   — while streaming
      {"type": "session_id", "content": "<uuid>"}    — sent first, so the
                                                        browser knows the id
      {"type": "done"}                               — stream finished
      {"type": "error",     "content": "<msg>"}      — on failure
    """
    sid = req.session_id.strip() or str(uuid.uuid4())
    if sid not in sessions:
        sessions[sid] = []

    history = sessions[sid]
    history.append({"role": "user", "content": req.message})

    def event(obj: dict) -> str:
        return f"data: {json.dumps(obj)}\n\n"

    def generate():
        # Send session_id immediately so the browser can store it
        yield event({"type": "session_id", "content": sid})

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
                temperature=0.5,
                max_tokens=512,
                stream=True,          # ← key difference from /chat
            )

            full_reply = ""
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    full_reply += token
                    yield event({"type": "delta", "content": token})

            # Save the complete reply to history once streaming is done
            history.append({"role": "assistant", "content": full_reply})
            yield event({"type": "done"})

        except AuthenticationError:
            yield event({"type": "error", "content": "Invalid OpenAI API key."})
        except RateLimitError:
            yield event({"type": "error", "content": "Rate limit exceeded. Try again shortly."})
        except Exception as e:
            yield event({"type": "error", "content": str(e)})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # prevents nginx from buffering SSE
        },
    )
