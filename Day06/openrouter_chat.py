"""
Day 06 — OpenRouter Chat Example
==================================
OpenRouter lets you call 100+ LLMs (GPT-4, Claude, Llama, Mistral …)
through a single, OpenAI-compatible API.

The only differences from the regular OpenAI SDK:
  1. base_url = "https://openrouter.ai/api/v1"
  2. api_key  = your OpenRouter key  (https://openrouter.ai/keys)
  3. model    = any model slug from  https://openrouter.ai/models

Everything else — messages format, streaming, parameters — is identical.

Setup
-----
  pip install openai python-dotenv
  Create a .env file:  OPENROUTER_API_KEY=sk-or-...

Run
---
  python openrouter_chat.py
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# ── 1. Configuration ─────────────────────────────────────────────────────────

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Set OPENROUTER_API_KEY in your .env file.")

# ── 2. Client setup — only base_url changes vs. regular OpenAI ───────────────

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Pick any model from https://openrouter.ai/models
# Free options: "meta-llama/llama-3.1-8b-instruct:free"
#               "mistralai/mistral-7b-instruct:free"
#               "google/gemma-3-1b-it:free"
MODEL = "meta-llama/llama-3.1-8b-instruct:free"

SYSTEM_PROMPT = "You are a helpful assistant. Be concise and friendly."

# ── 3. Chat function (streaming) ─────────────────────────────────────────────

def chat_stream(history: list[dict], user_message: str) -> str:
    """Send a message and stream the reply token by token. Returns full reply."""

    history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    # stream=True → response comes in chunks
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=512,
        stream=True,
    )

    print("\nAssistant: ", end="", flush=True)
    full_reply = ""

    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        print(token, end="", flush=True)   # print each token as it arrives
        full_reply += token

    print()  # newline after stream ends

    history.append({"role": "assistant", "content": full_reply})
    return full_reply


# ── 4. Main loop ─────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print(f"OpenRouter Chat  |  model: {MODEL}")
    print("Commands: 'quit' to exit, 'clear' to reset history")
    print("=" * 50)

    history = []   # stores {role, content} pairs for multi-turn context

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            history.clear()
            print("(History cleared)")
            continue

        chat_stream(history, user_input)


if __name__ == "__main__":
    main()
