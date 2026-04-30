"""
Day 06 Demo: Text Generation & Chatbots
========================================
Use case : Internal Help Desk Assistant
Model    : gpt-4.1
Features : system prompt, chat history, streaming, error handling

Setup:
  cp .env.example .env          # add your OPENAI_API_KEY
  pip install -r requirements.txt
  python day06_demo.py
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4.1"

# ---------------------------------------------------------------------------
# System prompt — defines the chatbot's persona and scope
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a helpful internal IT help desk assistant.
You answer employee questions about software tools, access issues, and company systems.
Be concise, friendly, and professional.
If you don't know the answer, say so and suggest contacting the IT team directly."""

# ---------------------------------------------------------------------------
# Core: send one turn, maintain history
# ---------------------------------------------------------------------------
def chat(history: list[dict], user_message: str) -> str:
    """
    Append the user message to history, send to the API, and return the reply.
    The full conversation context is passed on every call.
    """
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        temperature=0.5,
        max_tokens=512,
    )

    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    return reply


# ---------------------------------------------------------------------------
# Streaming variant — prints tokens as they arrive
# ---------------------------------------------------------------------------
def chat_stream(history: list[dict], user_message: str) -> str:
    """
    Same as chat() but streams tokens to stdout in real time.
    Returns the complete reply string.
    """
    history.append({"role": "user", "content": user_message})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        temperature=0.5,
        max_tokens=512,
        stream=True,
    )

    print("Assistant: ", end="", flush=True)
    reply_parts = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            reply_parts.append(delta)
    print()  # newline after streaming ends

    reply = "".join(reply_parts)
    history.append({"role": "assistant", "content": reply})
    return reply


# ---------------------------------------------------------------------------
# Interactive terminal chat loop
# ---------------------------------------------------------------------------
def run_chat_loop(use_streaming: bool = True):
    print("\n" + "=" * 55)
    print("  Day 06 Demo: IT Help Desk Assistant")
    print("  Type 'quit' or 'exit' to end the session.")
    print("  Type 'history' to print the conversation so far.")
    print("  Type 'clear' to start a fresh conversation.")
    print("=" * 55 + "\n")

    history: list[dict] = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if user_input.lower() == "history":
            print("\n--- Conversation History ---")
            for msg in history:
                role = msg["role"].capitalize()
                print(f"  {role}: {msg['content']}\n")
            continue

        if user_input.lower() == "clear":
            history.clear()
            print("Conversation cleared.\n")
            continue

        try:
            if use_streaming:
                chat_stream(history, user_input)
            else:
                reply = chat(history, user_input)
                print(f"Assistant: {reply}\n")

        except AuthenticationError:
            print("Error: Invalid API key. Check your .env file.")
            sys.exit(1)
        except RateLimitError:
            print("Error: Rate limit hit. Wait a moment and try again.")
        except APIConnectionError:
            print("Error: Cannot reach the API. Check your network connection.")
        except Exception as e:
            print(f"Unexpected error: {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Pass --no-stream to disable streaming for slower networks / debugging
    streaming = "--no-stream" not in sys.argv
    run_chat_loop(use_streaming=streaming)
