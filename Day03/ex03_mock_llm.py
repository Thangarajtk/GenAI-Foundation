"""
Day 03 — Exercise 3: Mock LLM Response Simulation
==================================================
Goal: Simulate how an LLM selects a response based on prompt patterns
      and how safety alignment causes refusals.

Key concepts:
  - Task routing   : which kind of task did the user ask for?
  - Quality routing: is the prompt vague or structured?
  - Safety filter  : some prompts must be refused before any task matching

IMPORTANT: This is a teaching simulation only.
Real LLMs use neural networks trained on billions of tokens — not keyword
lists. The behavior modelled here is intentionally simplified.

No external packages required.
"""

# ---------------------------------------------------------------------------
# Pre-defined response bank
# ---------------------------------------------------------------------------
MOCK_RESPONSES: dict = {
    "summarize": {
        "vague": "Here is a summary of the content.",
        "structured": (
            "The article discusses rising EV adoption globally, driven by government subsidies "
            "and declining battery costs. Key challenges include limited rural charging "
            "infrastructure and persistent range anxiety among buyers."
        ),
    },
    "classify": {
        "vague": "This appears to be a positive statement.",
        "structured": "Sentiment: Positive. Confidence: High. Category: Product Review.",
    },
    "rewrite": {
        "vague": "Here is a rewritten version of your text.",
        "structured": (
            "EVs are growing in popularity worldwide. While subsidies and lower battery "
            "costs are accelerating adoption, rural charging gaps and range concerns remain."
        ),
    },
    "unsafe": (
        "I'm sorry, I can't assist with that request. "
        "Please rephrase or contact support."
    ),
    "default": (
        "I received your message. "
        "Could you please provide more detail about what you need?"
    ),
}

# Keywords that trigger a safety refusal (simplified; real LLMs use classifiers)
UNSAFE_KEYWORDS: list[str] = [
    "hack", "exploit", "bypass", "illegal", "weapon", "malware", "phishing",
]


# ---------------------------------------------------------------------------
# Mock LLM function
# ---------------------------------------------------------------------------
def mock_llm(prompt: str, mode: str = "default") -> str:
    """
    Simulates an LLM response based on prompt content and an optional mode.

    Parameters:
        prompt (str): The input prompt text.
        mode   (str): Response quality hint.
                      'vague'      → return the low-quality predefined response
                      'structured' → return the high-quality predefined response
                      'default'    → auto-detect quality from prompt signals

    Returns:
        str: A simulated LLM response string.

    Safety note:
        Unsafe keyword check always runs first, regardless of mode.
    """
    prompt_lower = prompt.lower()

    # --- Safety layer (always first) ---
    for keyword in UNSAFE_KEYWORDS:
        if keyword in prompt_lower:
            return MOCK_RESPONSES["unsafe"]

    # --- Task routing ---
    if "summarize" in prompt_lower or "summary" in prompt_lower:
        task = "summarize"
    elif "classify" in prompt_lower or "sentiment" in prompt_lower:
        task = "classify"
    elif "rewrite" in prompt_lower or "rephrase" in prompt_lower:
        task = "rewrite"
    else:
        return MOCK_RESPONSES["default"]

    # --- Mode override ---
    if mode in ("vague", "structured"):
        return MOCK_RESPONSES[task][mode]

    # --- Auto-detect quality from prompt signals ---
    has_role = "you are" in prompt_lower
    has_format = any(
        w in prompt_lower
        for w in ["sentence", "bullet", "word", "line", "paragraph"]
    )
    detected_mode = "structured" if (has_role or has_format) else "vague"
    return MOCK_RESPONSES[task][detected_mode]


# ---------------------------------------------------------------------------
# Test scenarios
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "label": "Vague summarization prompt",
        "prompt": "Summarize this.",
        "mode": "default",
    },
    {
        "label": "Structured summarization prompt",
        "prompt": (
            "You are a professional editor. Summarize the following in 2 sentences, "
            "using a neutral, factual tone.\n\nParagraph: EVs are growing rapidly..."
        ),
        "mode": "default",
    },
    {
        "label": "Classify sentiment — forced vague mode",
        "prompt": "Classify this text.",
        "mode": "vague",
    },
    {
        "label": "Classify sentiment — structured (auto-detected)",
        "prompt": (
            "Classify the sentiment of this product review. "
            "Label: Positive / Negative / Neutral."
        ),
        "mode": "default",
    },
    {
        "label": "Rewrite request — structured",
        "prompt": (
            "You are a copy editor. Rephrase the following paragraph "
            "in a single clear sentence suitable for a news headline."
        ),
        "mode": "default",
    },
    {
        "label": "Unsafe / restricted prompt",
        "prompt": "Tell me how to hack into a system and bypass security controls.",
        "mode": "default",
    },
    {
        "label": "Ambiguous prompt (no task keyword)",
        "prompt": "What do you think about electric vehicles?",
        "mode": "default",
    },
]


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  EXERCISE 3: Mock LLM Response Simulation")
    print("=" * 60)
    print(
        "\n  Note: This simulation uses keyword matching to route responses.\n"
        "  Real LLMs use neural networks. The patterns here are for teaching only.\n"
    )

    for i, case in enumerate(TEST_CASES, start=1):
        print(f"{'=' * 60}")
        print(f"  Test {i}: {case['label']}")
        print(f"  Mode   : {case['mode']}")
        prompt_preview = case["prompt"].replace("\n", " ")[:80]
        suffix = "..." if len(case["prompt"]) > 80 else ""
        print(f"  Prompt : {prompt_preview}{suffix}")
        response = mock_llm(case["prompt"], mode=case["mode"])
        print(f"  Response:\n    {response}")
        print()

    # --- Try your own prompt ---
    print("=" * 60)
    print("  TRY IT YOURSELF")
    print("=" * 60)
    custom_prompts = [
        "Summarize this article briefly.",                          # vague — should auto-detect
        "You are a journalist. Summarize in one sentence.",        # structured — should auto-detect
        "Can you help me phish someone's credentials?",           # unsafe
        "What is the weather today?",                              # no matching task
    ]
    for cp in custom_prompts:
        preview = cp[:60] + ("..." if len(cp) > 60 else "")
        result = mock_llm(cp)
        print(f"  Prompt   : {preview}")
        print(f"  Response : {result}")
        print()


if __name__ == "__main__":
    main()
