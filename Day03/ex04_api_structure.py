"""
Day 03 — Exercise 4: API-Style Request and Response Understanding
=================================================================
Goal: Understand the structure of a real LLM API call by building and
      inspecting a toy request/response payload — without a live API.

Key concepts:
  - Request payload : what you send to the API
  - Response payload: what the API returns
  - Important fields: model, prompt, max_tokens, temperature, stop,
                      id, choices, finish_reason, usage

This prepares you for Day 05 where you will call real APIs.
No external packages required.
"""

import uuid
import datetime


# ---------------------------------------------------------------------------
# Mock API function
# ---------------------------------------------------------------------------
def mock_llm_api_call(request_payload: dict) -> dict:
    """
    Simulates an LLM API call.

    Accepts a request payload dictionary and returns a response payload
    dictionary structured like a real API response (OpenAI-style).

    Parameters:
        request_payload (dict): Must include at minimum 'prompt'.
                                Optional: model, max_tokens, temperature, stop.

    Returns:
        dict: Structured response with id, model, choices, usage.
    """
    # --- Extract request fields ---
    prompt = request_payload.get("prompt", "")
    max_tokens = request_payload.get("max_tokens", 100)
    temperature = request_payload.get("temperature", 0.7)
    model = request_payload.get("model", "mock-llm-v1")

    # --- Simulate response text based on prompt keywords ---
    prompt_lower = prompt.lower()
    if "summarize" in prompt_lower or "summary" in prompt_lower:
        response_text = (
            "EVs are gaining global traction due to government subsidies and falling "
            "battery costs, though rural charging gaps and range anxiety remain obstacles."
        )
    elif "translate" in prompt_lower:
        response_text = (
            "Les véhicules électriques sont de plus en plus populaires dans le monde entier."
        )
    elif "list" in prompt_lower or "bullet" in prompt_lower:
        response_text = (
            "1. Rising EV adoption\n"
            "2. Government incentives\n"
            "3. Charging infrastructure challenges"
        )
    else:
        response_text = "Thank you for your prompt. Here is a general response to your query."

    # --- Estimate token counts (word-split approximation) ---
    prompt_tokens = len(prompt.split())
    completion_tokens = min(len(response_text.split()), max_tokens)
    total_tokens = prompt_tokens + completion_tokens

    # --- Determine finish reason ---
    # "length"  → response was cut off at max_tokens
    # "stop"    → response ended naturally
    finish_reason = "length" if completion_tokens >= max_tokens else "stop"

    # --- Build structured response payload ---
    response_payload = {
        "id": f"mock-{uuid.uuid4().hex[:8]}",
        "object": "text_completion",
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        "model": model,
        "choices": [
            {
                "text": response_text,
                "index": 0,
                "finish_reason": finish_reason,
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
    }
    return response_payload


# ---------------------------------------------------------------------------
# Pretty-print helpers
# ---------------------------------------------------------------------------
def print_request(payload: dict) -> None:
    print("\n  === REQUEST PAYLOAD ===")
    for key, value in payload.items():
        if key == "prompt":
            preview = str(value).replace("\n", " ")[:60]
            print(f"    {key:<12}: {preview}...")
        else:
            print(f"    {key:<12}: {value}")


def print_response(payload: dict) -> None:
    print("\n  === RESPONSE PAYLOAD ===")
    print(f"    id           : {payload['id']}")
    print(f"    model        : {payload['model']}")
    print(f"    created      : {payload['created']}")
    print(f"\n    -- choices[0] --")
    choice = payload["choices"][0]
    print(f"    text         : {choice['text']}")
    print(f"    finish_reason: {choice['finish_reason']}")
    print(f"\n    -- usage --")
    for key, value in payload["usage"].items():
        print(f"    {key:<20}: {value}")


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
SCENARIOS = [
    {
        "label": "Summarization — conservative temperature",
        "request": {
            "model": "mock-llm-v1",
            "prompt": (
                "You are a news editor. Summarize the following in 2 sentences:\n\n"
                "Electric vehicles are becoming increasingly common worldwide as governments "
                "offer subsidies and battery costs continue to decline. However, rural charging "
                "infrastructure and range anxiety remain significant barriers to wider adoption."
            ),
            "max_tokens": 80,
            "temperature": 0.3,
            "stop": ["\n\n"],
        },
    },
    {
        "label": "Translation — balanced temperature",
        "request": {
            "model": "mock-llm-v1",
            "prompt": "Translate the following to French: EVs are popular worldwide.",
            "max_tokens": 60,
            "temperature": 0.7,
            "stop": ["."],
        },
    },
    {
        "label": "Bullet list — low max_tokens (will trigger 'length')",
        "request": {
            "model": "mock-llm-v1",
            "prompt": "List the top challenges for EV adoption as bullet points.",
            "max_tokens": 5,       # intentionally too low to demonstrate 'length' finish
            "temperature": 0.5,
            "stop": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  EXERCISE 4: API-Style Request and Response Understanding")
    print("=" * 60)
    print(
        "\n  Reminder — key request fields:\n"
        "    model       → which LLM to use\n"
        "    prompt      → your instruction or question\n"
        "    max_tokens  → hard cap on response length\n"
        "    temperature → 0 = deterministic, 1 = balanced, 2 = creative\n"
        "    stop        → sequences that end generation early\n"
    )

    for i, scenario in enumerate(SCENARIOS, start=1):
        print(f"\n{'=' * 60}")
        print(f"  Scenario {i}: {scenario['label']}")
        print_request(scenario["request"])
        response = mock_llm_api_call(scenario["request"])
        print_response(response)
        # Flag if response was truncated
        if response["choices"][0]["finish_reason"] == "length":
            print(
                "\n  ⚠ finish_reason='length' — response was cut off at max_tokens.\n"
                "    Increase max_tokens if you need a complete answer."
            )

    # --- Field explanation reference ---
    print(f"\n{'=' * 60}")
    print("  FIELD REFERENCE GUIDE")
    print(f"{'=' * 60}")
    reference = [
        ("temperature = 0.0", "Deterministic — always picks most likely token."),
        ("temperature = 0.7", "Balanced — good default for most tasks."),
        ("temperature = 1.5", "High variability — useful for creative tasks."),
        ("finish_reason=stop", "Model ended naturally."),
        ("finish_reason=length", "Hit max_tokens limit — answer may be incomplete."),
        ("finish_reason=content_filter", "Blocked by safety system."),
    ]
    for field, meaning in reference:
        print(f"  {field:<35} {meaning}")
    print()

    print("  TIP: In Day 05 you will replace mock_llm_api_call() with a real")
    print("  SDK call (e.g., openai.completions.create(**request)).")
    print("  The request and response shapes will look nearly identical.\n")


if __name__ == "__main__":
    main()
