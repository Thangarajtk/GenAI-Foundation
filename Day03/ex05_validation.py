"""
Day 03 — Exercise 5: Reflection and Output Validation
======================================================
Goal: Develop the habit of critically evaluating LLM output before using it.

Key concepts:
  - Human-in-the-Loop (HITL): a human reviews AI output before it is acted on
  - Hallucination: LLMs can produce confident-sounding but incorrect responses
  - High-stakes domains require extra scrutiny (medical, legal, financial)
  - Token efficiency matters for cost and latency

This exercise runs a validation checklist against a sample prompt/response pair
and prints a clear PASS / WARN report.

No external packages required.
"""

# ---------------------------------------------------------------------------
# Validation checklist function
# ---------------------------------------------------------------------------
def validate_llm_response(
    prompt: str,
    response_text: str,
    tokens_used: int,
    context_window: int = 4096,
) -> dict[str, bool]:
    """
    Runs a basic human-in-the-loop validation checklist on an LLM response.

    Parameters:
        prompt         : the prompt that was sent to the LLM
        response_text  : the response received from the LLM
        tokens_used    : total tokens consumed (prompt + response)
        context_window : size of the model's context window (default: 4096)

    Returns:
        dict mapping check description → True (PASS) / False (WARN)

    Note:
        These checks are heuristics for teaching. Production validation
        pipelines use more sophisticated NLP-based evaluators.
    """
    checklist: dict[str, bool] = {}

    # Check 1: Was the prompt reasonably structured?
    has_role = "you are" in prompt.lower()
    has_task = any(
        w in prompt.lower()
        for w in ["summarize", "classify", "translate", "list", "write", "explain"]
    )
    checklist["Prompt is clear and task-specific"] = has_role and has_task

    # Check 2: Does the response have a meaningful length?
    word_count = len(response_text.split())
    checklist[f"Response has meaningful length (> 5 words, got {word_count})"] = word_count > 5

    # Check 3: Does the response address the task keyword?
    task_words = ["summarize", "classify", "translate", "list", "explain", "write"]
    task_in_prompt = [w for w in task_words if w in prompt.lower()]
    # Rough heuristic: check that the response isn't just the default fallback
    is_generic = response_text.strip().lower().startswith("i received your message")
    checklist["Response appears task-relevant (not a generic fallback)"] = not is_generic

    # Check 4: High-stakes domain — always flag for human review
    high_stakes = ["medical", "legal", "financial", "diagnosis", "lawsuit", "investment",
                   "clinical", "prescription", "compliance", "regulatory"]
    in_high_stakes_domain = any(w in prompt.lower() for w in high_stakes)
    checklist["Human review recommended (high-stakes domain detected)"] = in_high_stakes_domain

    # Check 5: Token budget health
    usage_pct = (tokens_used / context_window) * 100
    checklist[
        f"Token usage is under 80% of context window ({usage_pct:.1f}% of {context_window})"
    ] = usage_pct < 80

    # Check 6: Was the response a refusal / safety block?
    refusal_phrases = ["i'm sorry", "i can't", "i cannot", "not able to assist",
                       "please rephrase", "contact support"]
    is_refusal = any(phrase in response_text.lower() for phrase in refusal_phrases)
    checklist["Response was not a safety refusal"] = not is_refusal

    # Check 7: Does the response contain uncertainty signals?
    uncertainty_phrases = ["i think", "i believe", "may be", "might be", "i'm not sure",
                           "approximately", "could be", "possibly"]
    has_uncertainty = any(phrase in response_text.lower() for phrase in uncertainty_phrases)
    # Uncertainty language is a WARN — it means the model is hedging
    checklist["Response does not contain excessive uncertainty language"] = not has_uncertainty

    return checklist


def print_checklist(checklist: dict[str, bool]) -> bool:
    """Prints the checklist and returns True if all checks passed."""
    all_passed = True
    warn_count = 0
    for description, passed in checklist.items():
        # High-stakes domain check: WARN when True (human review IS needed)
        if "high-stakes" in description.lower():
            if passed:
                status = "WARN"
                warn_count += 1
                all_passed = False
            else:
                status = "INFO"
        else:
            if passed:
                status = "PASS"
            else:
                status = "WARN"
                warn_count += 1
                all_passed = False
        print(f"    [{status:<4}]  {description}")
    return all_passed


# ---------------------------------------------------------------------------
# Test scenarios
# ---------------------------------------------------------------------------
SCENARIOS = [
    {
        "label": "Medical summary — well-formed prompt, high-stakes domain",
        "prompt": (
            "You are a medical information assistant. Summarize the following patient report "
            "in plain English for a general audience."
        ),
        "response": (
            "The patient shows signs of elevated blood pressure and mild inflammation. "
            "The doctor recommends lifestyle changes and a follow-up in 3 months."
        ),
        "tokens_used": 82,
    },
    {
        "label": "News summarization — good prompt, safe domain",
        "prompt": (
            "You are a news editor. Summarize the following article in 2 sentences, "
            "using a neutral tone."
        ),
        "response": (
            "EV adoption is rising globally due to government subsidies and declining battery costs. "
            "However, rural charging infrastructure and range anxiety remain key obstacles."
        ),
        "tokens_used": 55,
    },
    {
        "label": "Vague prompt — generic response",
        "prompt": "Summarize this.",
        "response": "Here is a summary of the content.",
        "tokens_used": 10,
    },
    {
        "label": "Safety refusal scenario",
        "prompt": "You are a security expert. Explain how to exploit web vulnerabilities.",
        "response": (
            "I'm sorry, I can't assist with that request. "
            "Please rephrase or contact support."
        ),
        "tokens_used": 20,
    },
    {
        "label": "Uncertain/hedging response",
        "prompt": "You are an analyst. Explain why EV stocks might rise.",
        "response": (
            "I think EV stocks may be trending upward. I believe government policy could "
            "be a factor, but I'm not sure of the exact timeline."
        ),
        "tokens_used": 38,
    },
    {
        "label": "Token overflow warning scenario",
        "prompt": "You are a researcher. Summarize this lengthy report.",
        "response": "The report covers several key findings about clean energy adoption.",
        "tokens_used": 3500,   # simulating a near-full context window
    },
]


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------
def main():
    print("=" * 65)
    print("  EXERCISE 5: Reflection and Output Validation")
    print("=" * 65)
    print(
        "\n  Human-in-the-Loop (HITL) means a human reviews AI output\n"
        "  before it is acted on. This checklist helps build that habit.\n"
        "\n  Legend:\n"
        "    [PASS] → Check succeeded\n"
        "    [WARN] → Requires attention before using the output\n"
        "    [INFO] → Informational note\n"
    )

    for i, scenario in enumerate(SCENARIOS, start=1):
        print(f"{'=' * 65}")
        print(f"  Scenario {i}: {scenario['label']}")
        print(f"    Prompt   : {scenario['prompt'][:70]}...")
        print(f"    Response : {scenario['response'][:70]}...")
        print(f"    Tokens   : {scenario['tokens_used']}")
        print()
        checklist = validate_llm_response(
            prompt=scenario["prompt"],
            response_text=scenario["response"],
            tokens_used=scenario["tokens_used"],
        )
        all_passed = print_checklist(checklist)
        print()
        if all_passed:
            print("    → All checks passed. Still verify facts independently.")
        else:
            print("    → One or more warnings raised. Review before using this output.")
        print()

    # --- Reflection questions ---
    print("=" * 65)
    print("  CLASS DISCUSSION QUESTIONS")
    print("=" * 65)
    questions = [
        "1. Why does the medical scenario flag a warning even with a good prompt and response?",
        "2. What other domains should always require human review?",
        "3. If finish_reason='length', what might be missing from the response?",
        "4. Can a confident-sounding response still be factually wrong? (Hallucination)",
        "5. What would happen if a medical AI response was used without any validation?",
    ]
    for q in questions:
        print(f"  {q}")
    print()


if __name__ == "__main__":
    main()
