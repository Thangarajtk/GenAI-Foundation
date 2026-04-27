"""
Day 03 — Exercise 2: Token and Context Window Intuition
=======================================================
Goal: Develop an intuitive feel for how tokens are counted and how
      prompts + responses consume a context window.

Key concepts:
  - Tokens are not the same as words
  - Context window = prompt tokens + history tokens + response tokens
  - Exceeding the window causes truncation or failure

No external packages required.
"""

import re


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------
def estimate_tokens(text: str) -> int:
    """
    Approximates token count by splitting on words and punctuation.

    Real tokenizers (BPE, SentencePiece, etc.) work differently — this
    is intentionally simplified to build intuition, not precision.

    Rule of thumb:  ~1 token per short word,
                    multi-syllable or rare words may be split into 2–3 tokens.
    """
    tokens = re.findall(r"\w+|[^\w\s]", text)
    return len(tokens)


# ---------------------------------------------------------------------------
# Context window status
# ---------------------------------------------------------------------------
def context_window_status(
    prompt_tokens: int,
    response_tokens: int,
    window_size: int = 4096,
) -> dict:
    """
    Returns a summary of how a prompt + response consume a context window.

    Parameters:
        prompt_tokens   : estimated tokens in the prompt
        response_tokens : estimated tokens in the response
        window_size     : total context window size (default: 4096)
    """
    total = prompt_tokens + response_tokens
    remaining = window_size - total
    usage_pct = round((total / window_size) * 100, 1)
    return {
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "total_tokens": total,
        "context_window": window_size,
        "remaining_tokens": remaining,
        "usage_percent": usage_pct,
        "fits_in_window": total <= window_size,
    }


def print_status(label: str, status: dict) -> None:
    fits = "YES" if status["fits_in_window"] else "NO — OVERFLOW!"
    print(f"\n  [{label}]")
    print(f"    Prompt tokens   : {status['prompt_tokens']}")
    print(f"    Response tokens : {status['response_tokens']}")
    print(f"    Total tokens    : {status['total_tokens']}")
    print(f"    Context window  : {status['context_window']}")
    print(f"    Remaining       : {status['remaining_tokens']}")
    print(f"    Usage           : {status['usage_percent']}%")
    print(f"    Fits in window  : {fits}")


# ---------------------------------------------------------------------------
# Sample texts
# ---------------------------------------------------------------------------
SHORT_PROMPT = "Summarize this article in one sentence."

LONG_PROMPT = (
    "You are an expert financial analyst. The following is a quarterly earnings\n"
    "report for a technology company. Please extract the top 5 key performance indicators,\n"
    "provide a trend analysis for revenue and operating income, identify any risk factors\n"
    "mentioned in the report, and suggest 3 questions a board member should ask the CFO.\n\n"
    "Report:\n"
    + "Revenue grew 12% year-over-year. Operating margins improved slightly. " * 50
)

MOCK_RESPONSE = (
    "Electric vehicles are gaining global traction, "
    "but charging infrastructure remains a key barrier."
)

# This simulates a conversation that has been going on for a while
CHAT_HISTORY = (
    "User: What are EVs?\n"
    "Assistant: Electric vehicles powered by batteries instead of combustion engines.\n"
    "User: Are they expensive?\n"
    "Assistant: Costs vary, but prices have dropped significantly in recent years.\n"
    "User: What about charging?\n"
    "Assistant: Urban charging is generally good; rural coverage is still limited.\n"
) * 10  # simulate 10 rounds of chat


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------
def main():
    print("=" * 55)
    print("  EXERCISE 2: Token and Context Window Intuition")
    print("=" * 55)

    # --- Token estimates ---
    short_tokens = estimate_tokens(SHORT_PROMPT)
    long_tokens = estimate_tokens(LONG_PROMPT)
    response_tokens = estimate_tokens(MOCK_RESPONSE)
    history_tokens = estimate_tokens(CHAT_HISTORY)

    print("\n--- Token Estimates ---")
    print(f"  Short prompt    : {short_tokens:>6} tokens")
    print(f"  Long prompt     : {long_tokens:>6} tokens")
    print(f"  Mock response   : {response_tokens:>6} tokens")
    print(f"  Chat history    : {history_tokens:>6} tokens  (10 rounds)")

    # --- Context window usage ---
    print("\n--- Context Window Usage (window = 4096 tokens) ---")
    print_status("Short prompt + response", context_window_status(short_tokens, response_tokens))
    print_status("Long prompt + response", context_window_status(long_tokens, response_tokens))
    print_status(
        "Chat history + short prompt + response",
        context_window_status(history_tokens + short_tokens, response_tokens),
    )

    # --- Different model window sizes ---
    print("\n--- Same long prompt across different model window sizes ---")
    models = [
        ("GPT-3.5 (4K window)", 4096),
        ("GPT-4 (128K window)", 128_000),
        ("Gemini 1.5 Pro (1M window)", 1_000_000),
    ]
    for model_name, window in models:
        status = context_window_status(long_tokens, response_tokens, window_size=window)
        fits = "OK" if status["fits_in_window"] else "OVERFLOW"
        print(f"  {model_name:<35} {status['usage_percent']:>5}% used   [{fits}]")

    print("\n--- Discussion Questions ---")
    questions = [
        "1. What happens when chat history fills most of the context window?",
        "2. Why do some apps summarize old messages instead of keeping full history?",
        "3. If max_tokens=50 but the ideal answer needs 200 tokens, what happens?",
    ]
    for q in questions:
        print(f"  {q}")
    print()


if __name__ == "__main__":
    main()
