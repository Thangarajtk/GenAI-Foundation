"""
Day 03 Exercises — Combined Runner
===================================
Run all five exercises in sequence from a single entry point.

Usage:
    python day03_exercises.py           # run all exercises
    python day03_exercises.py 1         # run only exercise 1
    python day03_exercises.py 3 4       # run exercises 3 and 4

Individual exercise files:
    ex01_prompt_quality.py
    ex02_token_estimation.py
    ex03_mock_llm.py
    ex04_api_structure.py
    ex05_validation.py

No external packages required.
"""

import sys

# Import each exercise's main() function
from ex01_prompt_quality import main as ex01
from ex02_token_estimation import main as ex02
from ex03_mock_llm import main as ex03
from ex04_api_structure import main as ex04
from ex05_validation import main as ex05

EXERCISES = {
    1: ("Prompt and Response Intuition", ex01),
    2: ("Token and Context Window Intuition", ex02),
    3: ("Mock LLM Response Simulation", ex03),
    4: ("API-Style Request and Response Understanding", ex04),
    5: ("Reflection and Output Validation", ex05),
}


def run_exercise(number: int) -> None:
    title, fn = EXERCISES[number]
    banner = f"  DAY 03 — EXERCISE {number}: {title}  "
    border = "=" * (len(banner) + 4)
    print(f"\n\n{border}")
    print(f"=={banner}==")
    print(f"{border}\n")
    fn()


def main():
    # Determine which exercises to run
    args = sys.argv[1:]
    if args:
        selected = []
        for arg in args:
            try:
                n = int(arg)
            except ValueError:
                print(f"  Invalid argument '{arg}'. Must be an integer between 1 and 5.")
                sys.exit(1)
            if n not in EXERCISES:
                print(f"  Exercise {n} does not exist. Choose from 1–5.")
                sys.exit(1)
            selected.append(n)
    else:
        selected = list(EXERCISES.keys())

    print("\n" + "=" * 60)
    print("  DAY 03 LAB: Understanding LLMs — Prompts, Tokens, APIs")
    print("=" * 60)
    print(f"  Running exercises: {selected}")
    print(f"  No API keys required. All exercises use mock data.")
    print("=" * 60)

    for n in selected:
        run_exercise(n)

    print("\n" + "=" * 60)
    print("  LAB COMPLETE")
    print("=" * 60)
    print("  Next step → Day 05: Real API Integration with OpenAI / Anthropic")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
