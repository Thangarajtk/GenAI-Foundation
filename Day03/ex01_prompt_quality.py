"""
Day 03 — Exercise 1: Prompt and Response Intuition
===================================================
Goal: Understand how prompt clarity affects response quality.

Key concepts:
  - Role instruction  ("You are a...")
  - Output format     ("in exactly 2 sentences")
  - Tone guidance     ("neutral, factual")
  - Clear task label  ("Summarize the following")

No external packages required.
"""

# ---------------------------------------------------------------------------
# Sample text used in both prompts
# ---------------------------------------------------------------------------
ARTICLE = (
    "Electric vehicles (EVs) are becoming more common on roads around the world. "
    "Governments are offering subsidies, and battery costs have dropped significantly "
    "over the last decade. However, charging infrastructure remains a challenge in "
    "rural areas, and range anxiety is still cited as a concern by potential buyers."
)

# ---------------------------------------------------------------------------
# Prompt definitions
# ---------------------------------------------------------------------------
vague_prompt = f"Summarize this.\n\n{ARTICLE}"

structured_prompt = (
    "You are a professional content editor.\n\n"
    "Summarize the following news paragraph in exactly 2 sentences.\n"
    "Your summary should be factual, neutral in tone, and suitable for a general audience.\n\n"
    f"Paragraph:\n{ARTICLE}"
)


# ---------------------------------------------------------------------------
# Prompt quality heuristic
# ---------------------------------------------------------------------------
def prompt_quality_check(prompt: str) -> str:
    """
    Returns a rough quality label (Low / Medium / High) based on whether
    the prompt includes a role, a format constraint, and a tone instruction.

    This is a teaching heuristic — not a real LLM evaluation.
    """
    has_role = "you are" in prompt.lower()
    has_format = any(
        word in prompt.lower()
        for word in ["sentence", "bullet", "list", "paragraph", "word"]
    )
    has_tone = any(
        word in prompt.lower()
        for word in ["neutral", "formal", "simple", "concise"]
    )
    score = sum([has_role, has_format, has_tone])
    labels = ["Low", "Medium", "High"]
    return labels[min(score, 2)]


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------
def main():
    print("=" * 55)
    print("  EXERCISE 1: Prompt and Response Intuition")
    print("=" * 55)

    print("\n--- Prompt 1: Vague ---\n")
    print(vague_prompt)
    quality = prompt_quality_check(vague_prompt)
    print(f"\n  >> Estimated Prompt Quality: {quality}")

    print("\n" + "-" * 55)

    print("\n--- Prompt 2: Structured ---\n")
    print(structured_prompt)
    quality = prompt_quality_check(structured_prompt)
    print(f"\n  >> Estimated Prompt Quality: {quality}")

    print("\n" + "=" * 55)
    print("  REFLECTION QUESTIONS")
    print("=" * 55)
    questions = [
        "1. What specific elements made Prompt 2 score higher?",
        "2. Could you rewrite Prompt 1 to score 'High' without changing the task?",
        "3. Which prompt would produce a more usable response in a real application?",
    ]
    for q in questions:
        print(f"  {q}")
    print()


if __name__ == "__main__":
    main()
