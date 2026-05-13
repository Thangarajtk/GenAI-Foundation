"""
Day 06 Chat App — FastAPI Backend with All Exercises
======================================================
POST /chat  →  send a message, get a reply
GET  /      →  health check & available personas/models
GET  /config  →  get available personas and models

Chat history is kept in memory per session_id with sliding window support.

EXERCISES IMPLEMENTED:
1. ✅ Change the persona (configurable SYSTEM_PROMPT)
2. ✅ Adjust temperature (configurable 0.0, 0.5, 1.0)
3. ✅ Add a message counter (tracked per session)
4. ✅ Limit history length (sliding context window)
5. ✅ Switch model (configurable model selection)
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

# =========================================================================
# EXERCISE 5: Configurable Model (default to a working modern model)
# =========================================================================
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]

# =========================================================================
# EXERCISE 1: Multiple Personas (System Prompts)
# =========================================================================
PERSONAS = {
    "it_helpdesk": {
        "name": "IT Help Desk",
        "system_prompt": (
            "You are a helpful internal IT Help Desk assistant. "
            "Answer employee questions about software tools, access issues, and company systems. "
            "Be concise, friendly, and professional. "
            "If you don't know the answer, say so and suggest contacting IT directly."
        ),
    },
    "hr_assistant": {
        "name": "HR Assistant",
        "system_prompt": (
            "You are a friendly and helpful HR Assistant. "
            "Help employees with questions about benefits, policies, leave, hiring, and company culture. "
            "Be empathetic, supportive, and professional. "
            "For sensitive matters, suggest they contact HR directly."
        ),
    },
    "onboarding_bot": {
        "name": "Onboarding Specialist",
        "system_prompt": (
            "You are an enthusiastic Onboarding Specialist Bot. "
            "Welcome new employees and help them get started by explaining company processes, tools, teams, and policies. "
            "Be welcoming, encouraging, and provide step-by-step guidance. "
            "Make them feel excited about joining the company."
        ),
    },
    "finance_helper": {
        "name": "Finance Helper",
        "system_prompt": (
            "You are a Finance Helper Assistant. "
            "Assist employees with questions about expense reports, budgeting, cost centers, and financial policies. "
            "Be accurate, clear, and professional. "
            "For complex matters, direct them to the Finance department."
        ),
    },
}

DEFAULT_PERSONA = "it_helpdesk"

# =========================================================================
# EXERCISE 2: Temperature Settings
# =========================================================================
TEMPERATURE_PRESETS = {
    "deterministic": 0.0,  # Same response every time
    "balanced": 0.5,       # Default - good balance
    "creative": 1.0,       # More varied and creative
}

DEFAULT_TEMPERATURE = 0.5

# =========================================================================
# EXERCISE 4: History Limiting (Sliding Context Window)
# =========================================================================
MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", "50"))  # Keep last 50 messages

# In-memory session store
# { session_id: {"history": [...], "message_count": 0, "persona": "...", "temperature": 0.5} }
sessions: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str = ""              # empty → server creates a new one
    persona: str = DEFAULT_PERSONA    # EXERCISE 1: Choose persona
    temperature: float = DEFAULT_TEMPERATURE  # EXERCISE 2: Choose temperature
    model: str = DEFAULT_MODEL        # EXERCISE 5: Choose model


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    history: list[dict]
    message_count: int                # EXERCISE 3: Message counter
    persona: str
    temperature: float
    model: str


class ConfigResponse(BaseModel):
    personas: dict
    models: list[str]
    temperature_presets: dict
    default_persona: str
    default_model: str
    default_temperature: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def health():
    return {"status": "ok", "service": "Day 06 Chatbot API"}


@app.get("/config")
def get_config():
    """EXERCISES: Get available configurations for all exercises."""
    return ConfigResponse(
        personas=PERSONAS,
        models=AVAILABLE_MODELS,
        temperature_presets=TEMPERATURE_PRESETS,
        default_persona=DEFAULT_PERSONA,
        default_model=DEFAULT_MODEL,
        default_temperature=DEFAULT_TEMPERATURE,
    )


def get_or_create_session(session_id: str, persona: str, temperature: float):
    """Create or retrieve session with EXERCISE 4: history limiting."""
    sid = session_id.strip() or str(uuid.uuid4())
    
    if sid not in sessions:
        sessions[sid] = {
            "history": [],
            "message_count": 0,
            "persona": persona,
            "temperature": temperature,
        }
    else:
        # Update persona/temperature if provided
        if persona:
            sessions[sid]["persona"] = persona
        if temperature:
            sessions[sid]["temperature"] = temperature
    
    return sid, sessions[sid]


def limit_history(history: list, max_length: int = MAX_HISTORY_LENGTH) -> list:
    """EXERCISE 4: Implement sliding context window - keep only last N messages."""
    if len(history) > max_length:
        return history[-max_length:]
    return history


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Resolve or create session
    sid, session_data = get_or_create_session(req.session_id, req.persona, req.temperature)
    
    history = session_data["history"]
    persona = session_data["persona"]
    temperature = session_data["temperature"]
    
    # Get the system prompt for the persona
    system_prompt = PERSONAS.get(persona, PERSONAS[DEFAULT_PERSONA])["system_prompt"]
    
    # EXERCISE 3: Increment message counter
    history.append({"role": "user", "content": req.message})
    session_data["message_count"] += 1

    # EXERCISE 4: Limit history length
    session_data["history"] = limit_history(history)
    history = session_data["history"]

    try:
        resp = client.chat.completions.create(
            model=req.model,
            messages=[{"role": "system", "content": system_prompt}] + history,
            temperature=temperature,
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
    
    # EXERCISE 4: Apply history limit to stored history too
    history = limit_history(history)
    session_data["history"] = history
    
    return ChatResponse(
        reply=reply,
        session_id=sid,
        history=history,
        message_count=session_data["message_count"],
        persona=persona,
        temperature=temperature,
        model=req.model,
    )


@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"cleared": session_id}


# ---------------------------------------------------------------------------
# Streaming endpoint with all exercises
# ---------------------------------------------------------------------------
@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """
    Same as /chat but returns a text/event-stream response.
    
    EXERCISES IMPLEMENTED:
    1. ✅ Persona: System prompt changes based on persona
    2. ✅ Temperature: Controlled by request parameter
    3. ✅ Message counter: Tracked and returned
    4. ✅ History limiting: Sliding context window applied
    5. ✅ Model: Chosen based on request parameter

    Each Server-Sent Event carries one JSON object:
      {"type": "delta",      "content": "<token>"}   — while streaming
      {"type": "session_id", "content": "<uuid>"}    — sent first
      {"type": "done"}                               — stream finished
      {"type": "error",     "content": "<msg>"}      — on failure
    """
    sid, session_data = get_or_create_session(req.session_id, req.persona, req.temperature)
    
    history = session_data["history"]
    persona = session_data["persona"]
    temperature = session_data["temperature"]
    
    # Get the system prompt for the persona
    system_prompt = PERSONAS.get(persona, PERSONAS[DEFAULT_PERSONA])["system_prompt"]
    
    # EXERCISE 3: Increment message counter
    history.append({"role": "user", "content": req.message})
    session_data["message_count"] += 1

    # EXERCISE 4: Limit history length
    session_data["history"] = limit_history(history)
    history = session_data["history"]

    def event(obj: dict) -> str:
        return f"data: {json.dumps(obj)}\n\n"

    def generate():
        # Send session metadata immediately
        yield event({
            "type": "session_id",
            "content": sid,
            "message_count": session_data["message_count"],
            "persona": persona,
            "temperature": temperature,
            "model": req.model,
        })

        try:
            stream = client.chat.completions.create(
                model=req.model,
                messages=[{"role": "system", "content": system_prompt}] + history,
                temperature=temperature,
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
            
            # EXERCISE 4: Apply history limit to stored history too
            session_data["history"] = limit_history(history)
            
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
