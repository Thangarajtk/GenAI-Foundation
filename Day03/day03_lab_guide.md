# Day 03 Lab Guide: Understanding LLMs — Prompts, Tokens, and API Basics

---

## Lab Objectives

By the end of this lab, learners will be able to:

- Explain how a prompt travels to an LLM and how a response is generated
- Distinguish between a vague prompt and a well-structured prompt
- Estimate token count and understand why context windows matter
- Simulate LLM responses using mock Python code
- Read and interpret a structured API-style request and response payload
- Apply basic human-in-the-loop validation thinking to LLM outputs

---

## Learning Outcomes

| # | Outcome |
|---|---------|
| 1 | Understand the prompt-to-response flow at a conceptual level |
| 2 | Write clearer prompts and predict why they produce better responses |
| 3 | Estimate token usage and relate it to context window limits |
| 4 | Simulate mock LLM behavior using Python without a real API |
| 5 | Interpret key LLM API request fields: `prompt`, `max_tokens`, `temperature`, `model` |
| 6 | Recognize when LLM output requires human review or validation |

---

## Target Audience

Beginners and early learners in Generative AI / LLM fundamentals.  
No prior ML or NLP experience is required.

---

## Prerequisites

- Basic Python knowledge (functions, dictionaries, print statements)
- Day 01 and Day 02 concepts completed (Python basics, data handling)
- Python 3.8+ installed on your laptop
- No API keys or internet connection required for this lab

> **Note for instructors:** This lab is intentionally lightweight and offline-safe. Day 05 covers real API integration with live endpoints. Keep this lab focused on understanding, not implementation.

---

## Lab Setup

### Step 1: Confirm your Python environment

```bash
python --version
```

Expected output:
```
Python 3.10.x  (or 3.8 / 3.9 / 3.11 — all are fine)
```

### Step 2: Create the lab working directory

```bash
mkdir -p Day03
cd Day03
```

### Step 3: Create a lab script file

```bash
touch day03_exercises.py
```

You will add code from each exercise into this file, or run each block separately in a Python REPL / Jupyter notebook.

### Step 4: No additional packages needed

All exercises in this lab use only Python's standard library. No `pip install` is required.

---

## Lab Overview

```
Exercise 1  →  Prompt clarity and response quality intuition
Exercise 2  →  Token counting and context window intuition
Exercise 3  →  Mock LLM response simulation
Exercise 4  →  API-style request and response structure
Exercise 5  →  Reflection and output validation
```

**Estimated time:** 45–60 minutes  
**Format:** Instructor-led with individual hands-on steps

---

## Exercise 1: Prompt and Response Intuition

### Concept

When you interact with an LLM, the quality of your **prompt** (the instruction you send) has a direct impact on the quality of the **response** you receive.

A vague prompt gives the model too much freedom — it may produce something technically correct but not useful for your task. A clear, structured prompt guides the model toward the answer you actually need.

This is called **prompt engineering** — a skill you will develop across this training program.

### How the flow works

```
You (user)
    │
    ▼
[Prompt] ──► LLM processes tokens ──► [Response]
    ▲                                       │
    └───────── context window ──────────────┘
```

The model does not "think" like a human. It predicts the most likely next tokens based on your prompt and its training data.

---

### Task

Read the two prompts below for the **same task** (summarizing a news article). Discuss with your neighbor which one will likely produce a better response and why.

**Vague Prompt:**
```
Summarize this.

Electric vehicles (EVs) are becoming more common on roads around the world.
Governments are offering subsidies, and battery costs have dropped significantly
over the last decade. However, charging infrastructure remains a challenge in
rural areas, and range anxiety is still cited as a concern by potential buyers.
```

**Clear and Structured Prompt:**
```
You are a professional content editor.

Summarize the following news paragraph in exactly 2 sentences.
Your summary should be factual, neutral in tone, and suitable for a general audience.

Paragraph:
Electric vehicles (EVs) are becoming more common on roads around the world.
Governments are offering subsidies, and battery costs have dropped significantly
over the last decade. However, charging infrastructure remains a challenge in
rural areas, and range anxiety is still cited as a concern by potential buyers.
```

---

### Python Exercise

Run this code to print both prompts and a mock "quality score" comment:

```python
# Exercise 1: Prompt quality comparison

vague_prompt = """Summarize this.

Electric vehicles (EVs) are becoming more common on roads around the world.
Governments are offering subsidies, and battery costs have dropped significantly
over the last decade. However, charging infrastructure remains a challenge in
rural areas, and range anxiety is still cited as a concern by potential buyers."""

structured_prompt = """You are a professional content editor.

Summarize the following news paragraph in exactly 2 sentences.
Your summary should be factual, neutral in tone, and suitable for a general audience.

Paragraph:
Electric vehicles (EVs) are becoming more common on roads around the world.
Governments are offering subsidies, and battery costs have dropped significantly
over the last decade. However, charging infrastructure remains a challenge in
rural areas, and range anxiety is still cited as a concern by potential buyers."""


def prompt_quality_check(prompt):
    has_role = "you are" in prompt.lower()
    has_format = any(word in prompt.lower() for word in ["sentence", "bullet", "list", "paragraph", "word"])
    has_tone = any(word in prompt.lower() for word in ["neutral", "formal", "simple", "concise"])
    score = sum([has_role, has_format, has_tone])
    labels = ["Low", "Medium", "High"]
    return labels[score] if score < 3 else "High"


print("=== Prompt 1: Vague ===")
print(vague_prompt)
print(f"\nEstimated Quality: {prompt_quality_check(vague_prompt)}\n")

print("=" * 50)

print("\n=== Prompt 2: Structured ===")
print(structured_prompt)
print(f"\nEstimated Quality: {prompt_quality_check(structured_prompt)}\n")
```

### Expected Output

```
=== Prompt 1: Vague ===
Summarize this.

Electric vehicles (EVs) are becoming more common ...

Estimated Quality: Low

==================================================

=== Prompt 2: Structured ===
You are a professional content editor.
...

Estimated Quality: High
```

### Key Explanation Points

| Element | Why it matters |
|---------|----------------|
| **Role instruction** (`You are a...`) | Sets the persona and expertise level for the model |
| **Output format** (`2 sentences`) | Controls length and structure of the response |
| **Tone guidance** (`neutral, factual`) | Reduces ambiguity about style |
| **Clear task label** (`Summarize the following`) | Removes guesswork about what action is needed |

> **Instructor note:** Ask the class to rewrite the vague prompt in a better version before revealing the structured version. Discuss the difference in 2–3 minutes.

---

## Exercise 2: Token and Context Window Intuition

### Concept

LLMs do not read words — they read **tokens**.

A token is roughly a word, a part of a word, or a punctuation mark, depending on the model's tokenizer. Here are some approximate rules of thumb:

| Unit | Approximate tokens |
|------|-------------------|
| 1 short word | 1 token |
| 1 average English sentence | 15–25 tokens |
| 1 paragraph (100 words) | 120–140 tokens |
| 1 page of text (~500 words) | 600–750 tokens |

> These are approximations. Real tokenization depends on the model (GPT-4, Claude, Gemini, etc. each have different tokenizers).

### What is a context window?

The **context window** is the maximum number of tokens the model can "see" at one time.  
This includes:

- Your prompt
- Any conversation history
- The model's response

If your prompt + response exceeds the context window, the model either truncates input or fails.

```
Context Window (e.g., 4096 tokens total)
┌────────────────────────────────────────────┐
│  System instructions  (100 tokens)         │
│  Conversation history (500 tokens)         │
│  Your new prompt      (300 tokens)         │
│  ─────────────────────────────────────── │
│  Available for response: 3196 tokens       │
└────────────────────────────────────────────┘
```

---

### Python Exercise

```python
# Exercise 2: Token estimation

def estimate_tokens(text):
    """
    Simple approximation: count words and punctuation as tokens.
    Real tokenizers are more complex, but this gives useful intuition.
    """
    import re
    # Split on whitespace and punctuation
    tokens = re.findall(r"\w+|[^\w\s]", text)
    return len(tokens)


def context_window_status(prompt_tokens, response_tokens, window_size=4096):
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


# Sample texts
short_prompt = "Summarize this article in one sentence."

long_prompt = """You are an expert financial analyst. The following is a quarterly earnings
report for a technology company. Please extract the top 5 key performance indicators,
provide a trend analysis for revenue and operating income, identify any risk factors
mentioned in the report, and suggest 3 questions a board member should ask the CFO.

Report:
""" + ("Revenue grew 12% year-over-year. Operating margins improved slightly. " * 50)

mock_response = "Electric vehicles are gaining global traction, but charging infrastructure remains a key barrier."

# Estimate tokens
short_tokens = estimate_tokens(short_prompt)
long_tokens = estimate_tokens(long_prompt)
response_tokens = estimate_tokens(mock_response)

print(f"Short prompt token estimate : {short_tokens}")
print(f"Long prompt token estimate  : {long_tokens}")
print(f"Response token estimate     : {response_tokens}")
print()

# Context window check
print("--- Short prompt context usage ---")
status = context_window_status(short_tokens, response_tokens)
for key, value in status.items():
    print(f"  {key}: {value}")

print()
print("--- Long prompt context usage ---")
status = context_window_status(long_tokens, response_tokens)
for key, value in status.items():
    print(f"  {key}: {value}")
```

### Expected Output

```
Short prompt token estimate : 8
Long prompt token estimate  : 570
Response token estimate     : 18

--- Short prompt context usage ---
  prompt_tokens: 8
  response_tokens: 18
  total_tokens: 26
  context_window: 4096
  remaining_tokens: 4070
  usage_percent: 0.6
  fits_in_window: True

--- Long prompt context usage ---
  prompt_tokens: 570
  response_tokens: 18
  total_tokens: 588
  context_window: 4096
  remaining_tokens: 3508
  usage_percent: 14.4
  fits_in_window: True
```

### Discussion Points

- What happens when you include a 50-page PDF as context?
- What happens in a long multi-turn chat where history accumulates?
- Why do some applications summarize older history to save token budget?

> **Instructor note:** Mention that GPT-3.5 had a 4K token window, GPT-4 expanded to 128K, and Gemini 1.5 Pro supports 1M tokens. The principles are the same regardless of size.

---

## Exercise 3: Mock LLM Response Simulation

### Concept

In this exercise, you will create a Python function that **simulates** LLM behavior without calling a real API.

This helps you understand:
- How prompt patterns affect response selection
- How safety alignment causes refusals
- Why a generic prompt produces a generic response

This is **not** how real LLMs work internally — they use deep neural networks. This simulation is a teaching tool only.

---

### Python Exercise

```python
# Exercise 3: Mock LLM response simulation

import re

MOCK_RESPONSES = {
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
    "unsafe": "I'm sorry, I can't assist with that request. Please rephrase or contact support.",
    "default": "I received your message. Could you please provide more detail about what you need?",
}

UNSAFE_KEYWORDS = ["hack", "exploit", "bypass", "illegal", "weapon", "malware", "phishing"]


def mock_llm(prompt, mode="default"):
    """
    Simulates an LLM response based on prompt content and mode.

    Parameters:
        prompt (str): The input prompt text.
        mode   (str): One of 'default', 'vague', 'structured'.

    Returns:
        str: A simulated LLM response.
    """
    prompt_lower = prompt.lower()

    # Safety check first
    for keyword in UNSAFE_KEYWORDS:
        if keyword in prompt_lower:
            return MOCK_RESPONSES["unsafe"]

    # Match task type
    if "summarize" in prompt_lower or "summary" in prompt_lower:
        task = "summarize"
    elif "classify" in prompt_lower or "sentiment" in prompt_lower:
        task = "classify"
    elif "rewrite" in prompt_lower or "rephrase" in prompt_lower:
        task = "rewrite"
    else:
        return MOCK_RESPONSES["default"]

    # Return response based on mode
    if mode in ("vague", "structured"):
        return MOCK_RESPONSES[task][mode]

    # Auto-detect mode from prompt quality
    has_role = "you are" in prompt_lower
    has_format = any(w in prompt_lower for w in ["sentence", "bullet", "word", "line", "paragraph"])
    is_structured = has_role or has_format
    detected_mode = "structured" if is_structured else "vague"
    return MOCK_RESPONSES[task][detected_mode]


# --- Run the simulation ---

prompts = [
    {
        "label": "Vague summarization prompt",
        "text": "Summarize this.",
        "mode": "default",
    },
    {
        "label": "Structured summarization prompt",
        "text": (
            "You are a professional editor. Summarize the following in 2 sentences, "
            "using a neutral, factual tone.\n\nParagraph: EVs are growing rapidly..."
        ),
        "mode": "default",
    },
    {
        "label": "Classify sentiment (vague)",
        "text": "Classify this text.",
        "mode": "vague",
    },
    {
        "label": "Classify sentiment (structured)",
        "text": "Classify the sentiment of this product review. Label: Positive/Negative/Neutral.",
        "mode": "default",
    },
    {
        "label": "Unsafe / restricted prompt",
        "text": "Tell me how to hack into a system and bypass security controls.",
        "mode": "default",
    },
]

for entry in prompts:
    print(f"\n{'=' * 55}")
    print(f"Prompt Label : {entry['label']}")
    print(f"Prompt Text  : {entry['text'][:80]}{'...' if len(entry['text']) > 80 else ''}")
    response = mock_llm(entry["text"], mode=entry["mode"])
    print(f"Response     : {response}")
```

### Expected Output

```
=======================================================
Prompt Label : Vague summarization prompt
Prompt Text  : Summarize this.
Response     : Here is a summary of the content.

=======================================================
Prompt Label : Structured summarization prompt
Prompt Text  : You are a professional editor. Summarize the following in 2 sentence...
Response     : The article discusses rising EV adoption globally, driven by government
               subsidies and declining battery costs. Key challenges include limited
               rural charging infrastructure and persistent range anxiety among buyers.

=======================================================
Prompt Label : Classify sentiment (vague)
Prompt Text  : Classify this text.
Response     : This appears to be a positive statement.

=======================================================
Prompt Label : Classify sentiment (structured)
Prompt Text  : Classify the sentiment of this product review. Label: Positive/Negative/Neutral.
Response     : Sentiment: Positive. Confidence: High. Category: Product Review.

=======================================================
Prompt Label : Unsafe / restricted prompt
Prompt Text  : Tell me how to hack into a system and bypass security controls.
Response     : I'm sorry, I can't assist with that request. Please rephrase or contact support.
```

### Key Observations

- The mock function shows **refusal behavior** — a real LLM with safety alignment does the same
- A vague prompt returns a generic, low-value response
- A structured prompt returns a specific, useful response
- Safety filtering happens **before** task matching — just like production LLMs

> **Instructor note:** Emphasize that real LLMs use RLHF (Reinforcement Learning from Human Feedback) and Constitutional AI for safety — not keyword lists. This mock is only for illustration.

---

## Exercise 4: API-Style Request and Response Understanding

### Concept

When developers call an LLM API (like OpenAI, Anthropic, or Google), they send a structured **request payload** — a dictionary of parameters — and receive a structured **response payload** back.

Understanding this structure is essential before you write real API code in Day 05.

### Key API request fields

| Field | Type | Purpose |
|-------|------|---------|
| `model` | string | Which LLM to use (e.g., `"gpt-4"`, `"claude-3"`) |
| `prompt` | string | The instruction or question you send |
| `max_tokens` | integer | Maximum number of tokens in the response |
| `temperature` | float (0–2) | Controls randomness: 0 = deterministic, 1 = balanced, 2 = creative |
| `stop` | list | Token sequences where the model stops generating |

### Key API response fields

| Field | Type | Purpose |
|-------|------|---------|
| `id` | string | Unique identifier for this request |
| `model` | string | Model that was used |
| `choices` | list | One or more candidate responses |
| `text` | string | The actual generated response text |
| `finish_reason` | string | Why generation stopped (`"stop"`, `"length"`, `"content_filter"`) |
| `usage` | dict | Token counts for billing/monitoring |

---

### Python Exercise

```python
# Exercise 4: API-style request and response structure

import uuid
import datetime


def mock_llm_api_call(request_payload):
    """
    Simulates an LLM API call using a structured request payload.
    Returns a structured response payload (no real API is called).
    """

    # Extract fields from request
    prompt = request_payload.get("prompt", "")
    max_tokens = request_payload.get("max_tokens", 100)
    temperature = request_payload.get("temperature", 0.7)
    model = request_payload.get("model", "mock-llm-v1")

    # Simulate response text based on prompt content
    prompt_lower = prompt.lower()
    if "summarize" in prompt_lower:
        response_text = (
            "EVs are gaining global traction due to government subsidies and falling "
            "battery costs, though rural charging gaps and range anxiety remain obstacles."
        )
    elif "translate" in prompt_lower:
        response_text = "Les véhicules électriques sont de plus en plus populaires dans le monde entier."
    elif "list" in prompt_lower or "bullet" in prompt_lower:
        response_text = "1. Rising EV adoption\n2. Government incentives\n3. Charging infrastructure challenges"
    else:
        response_text = "Thank you for your prompt. Here is a general response to your query."

    # Estimate token counts (simplified)
    prompt_tokens = len(prompt.split())
    completion_tokens = min(len(response_text.split()), max_tokens)
    total_tokens = prompt_tokens + completion_tokens

    # Determine finish reason
    if completion_tokens >= max_tokens:
        finish_reason = "length"
    elif temperature > 1.5:
        finish_reason = "stop"
    else:
        finish_reason = "stop"

    # Build structured response
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


# --- Build and send a mock API request ---

request = {
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
}

print("=== REQUEST PAYLOAD ===")
for key, value in request.items():
    if key == "prompt":
        print(f"  {key}: {str(value)[:60]}...")
    else:
        print(f"  {key}: {value}")

response = mock_llm_api_call(request)

print("\n=== RESPONSE PAYLOAD ===")
print(f"  id      : {response['id']}")
print(f"  model   : {response['model']}")
print(f"  created : {response['created']}")
print(f"\n  --- choices[0] ---")
print(f"  text          : {response['choices'][0]['text']}")
print(f"  finish_reason : {response['choices'][0]['finish_reason']}")
print(f"\n  --- usage ---")
for key, value in response["usage"].items():
    print(f"  {key}: {value}")
```

### Expected Output

```
=== REQUEST PAYLOAD ===
  model: mock-llm-v1
  prompt: You are a news editor. Summarize the following in 2 se...
  max_tokens: 80
  temperature: 0.3
  stop: ['\n\n']

=== RESPONSE PAYLOAD ===
  id      : mock-3a9f1b2c
  model   : mock-llm-v1
  created : 2026-04-27T10:15:42Z

  --- choices[0] ---
  text          : EVs are gaining global traction due to government subsidies and falling
                  battery costs, though rural charging gaps and range anxiety remain obstacles.
  finish_reason : stop

  --- usage ---
  prompt_tokens: 55
  completion_tokens: 27
  total_tokens: 82
```

### Field-by-field explanation

```
temperature = 0.0   → Always picks the most likely next token. Deterministic.
temperature = 0.7   → Balanced creativity. Good for most tasks.
temperature = 1.5   → High variability. Good for creative writing.

max_tokens = 50     → Hard cap on response length.
                       If the answer needs 200 tokens, it will be cut off.

finish_reason:
  "stop"            → Model naturally completed the response.
  "length"          → Hit max_tokens before finishing.
  "content_filter"  → Blocked by safety system.
```

> **Instructor note:** In Day 05, learners will send real API calls using the `openai` or `anthropic` Python SDK. The request and response structure will look very similar to what they built here.

---

## Exercise 5: Reflection and Validation

### Concept

LLMs are powerful, but they are not always correct. Before using an LLM response in any real workflow, a human should validate it.

This is called **Human-in-the-Loop (HITL)** validation.

Ask yourself:
1. Was my prompt clear enough?
2. Does the response actually answer what I asked?
3. Is this response factually correct — or could it be a hallucination?
4. Could the response harm someone if it is wrong?
5. Am I using too many tokens for this task?

---

### Python Exercise

```python
# Exercise 5: Output reflection and validation checklist

def validate_llm_response(prompt, response_text, max_tokens_used, context_window=4096):
    """
    A simple reflection checklist for evaluating an LLM response.
    Learners should review each check and discuss with their team.
    """

    checklist = {}

    # Check 1: Was the prompt reasonably detailed?
    has_role = "you are" in prompt.lower()
    has_task = any(w in prompt.lower() for w in ["summarize", "classify", "translate", "list", "write"])
    checklist["Prompt is clear and task-specific"] = has_role and has_task

    # Check 2: Did the response seem to match the task?
    response_length = len(response_text.split())
    checklist["Response has reasonable length (> 5 words)"] = response_length > 5

    # Check 3: Human review needed?
    high_stakes_words = ["medical", "legal", "financial", "diagnosis", "lawsuit", "investment"]
    needs_human_review = any(w in prompt.lower() for w in high_stakes_words)
    checklist["Human review recommended (high-stakes domain)"] = needs_human_review

    # Check 4: Token budget concern?
    token_usage_pct = (max_tokens_used / context_window) * 100
    checklist[f"Token usage is under 80% of context window ({token_usage_pct:.1f}% used)"] = token_usage_pct < 80

    # Check 5: Was the response a refusal?
    refusal_phrases = ["i'm sorry", "i can't", "i cannot", "not able to assist"]
    is_refusal = any(phrase in response_text.lower() for phrase in refusal_phrases)
    checklist["Response was not a refusal/safety block"] = not is_refusal

    return checklist


# --- Test it ---

sample_prompt = (
    "You are a medical information assistant. Summarize the following patient report "
    "in plain English for a general audience."
)

sample_response = (
    "The patient shows signs of elevated blood pressure and mild inflammation. "
    "The doctor recommends lifestyle changes and a follow-up in 3 months."
)

token_usage = 82  # from Exercise 4

results = validate_llm_response(sample_prompt, sample_response, token_usage)

print("=== LLM OUTPUT VALIDATION CHECKLIST ===\n")
all_passed = True
for check, passed in results.items():
    status = "PASS" if passed else "WARN"
    if not passed:
        all_passed = False
    print(f"  [{status}]  {check}")

print()
if all_passed:
    print("  All checks passed. Proceed with caution — always verify facts independently.")
else:
    print("  One or more checks raised a warning. Review before using this output.")
```

### Expected Output

```
=== LLM OUTPUT VALIDATION CHECKLIST ===

  [PASS]  Prompt is clear and task-specific
  [PASS]  Response has reasonable length (> 5 words)
  [WARN]  Human review recommended (high-stakes domain)
  [PASS]  Token usage is under 80% of context window (2.0% used)
  [PASS]  Response was not a refusal/safety block

  One or more checks raised a warning. Review before using this output.
```

### Reflection Discussion (Instructor-led, 5 minutes)

Ask the class:

1. Why did the medical domain trigger a warning even though the prompt and response looked fine?
2. What other domains should always require human review?
3. If a response is returned with `finish_reason = "length"`, what does that mean for your output?
4. Can you trust a well-structured response that looks correct but was generated by an AI?
5. What would happen if this response was used directly without any validation?

> **Instructor note:** Use this exercise to introduce the concept of **hallucination** — LLMs can produce confident-sounding but factually incorrect responses. Validation is always important, especially in regulated or high-stakes domains.

---

## Key Observations

After completing all exercises, you should have observed the following:

| Observation | Why it matters |
|-------------|---------------|
| Vague prompts return generic, low-value responses | Prompt quality directly controls output quality |
| Structured prompts with role + format + tone instructions return better responses | Prompt engineering is a learnable, repeatable skill |
| Tokens are the unit of measurement for LLM input and output | You need to budget tokens just like memory in a program |
| Context windows have a fixed limit | Overflowing the context causes truncation or errors |
| Safety alignment causes refusals on restricted topics | LLMs are designed to be safe by default — refusals are expected behavior |
| API requests are structured payloads with clear fields | Understanding the API contract makes Day 05 integration much easier |
| LLM outputs must be validated by humans, especially in high-stakes domains | AI is a tool — human judgment is still essential |

---

## Troubleshooting Tips

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `SyntaxError` on f-string | Python version < 3.6 | Upgrade to Python 3.8+ |
| `ModuleNotFoundError: uuid` or `re` | Not installed | Both are standard library — no install needed |
| Mock responses always return "default" | Prompt doesn't contain expected keywords | Check for "summarize", "classify", or "rewrite" in your prompt |
| Token estimate seems too low | Our `estimate_tokens` splits on whitespace only | Real tokenizers split differently — this is intentional approximation |
| `finish_reason` shows `"length"` | `max_tokens` is set too low | Increase `max_tokens` in the request payload |
| Unsafe prompt not being caught | Keyword not in `UNSAFE_KEYWORDS` list | Add the keyword to the list, or modify the check condition |

---

## Summary / Recap

In this lab, you explored how LLMs work at a conceptual and structural level — without needing a real API key or internet connection.

### What you built and learned

| Exercise | What you did | What you learned |
|----------|-------------|-----------------|
| Exercise 1 | Compared vague vs. structured prompts | Prompt clarity directly controls output quality |
| Exercise 2 | Estimated token counts and context usage | Tokens are the unit of LLM consumption; context windows are finite |
| Exercise 3 | Simulated LLM responses with `mock_llm()` | How prompt patterns and safety alignment affect responses |
| Exercise 4 | Built and interpreted API request/response payloads | The structure of real LLM API calls before using them in Day 05 |
| Exercise 5 | Applied a validation checklist to LLM output | Why human-in-the-loop review is essential for AI outputs |

### What comes next

| Day | Topic |
|-----|-------|
| Day 03 (today) | Concepts: prompts, tokens, context, API structure, safety ✓ |
| Day 04 | Embeddings, semantic search, and vector representations |
| Day 05 | Real API integration: calling OpenAI / Anthropic APIs in Python |

> **Key takeaway:** Every real-world LLM application you will build in Day 05 and beyond depends on the foundational concepts you practiced today. Prompt clarity, token budgeting, safety awareness, and API structure understanding are the building blocks.

---

*Lab guide version: Day 03 — GenAI Foundation Training Program*  
*Estimated duration: 45–60 minutes*  
*No external APIs or API keys required*
