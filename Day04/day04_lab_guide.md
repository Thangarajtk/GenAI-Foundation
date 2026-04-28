# Day 04 Lab Guide: Prompt Engineering Fundamentals

---

## Lab Objectives

By the end of this lab, learners will be able to:
- Recognize the difference between weak and strong prompts
- Add context, constraints, and structure to prompts for better LLM outputs
- Use delimiters and specify output formats
- Apply zero-shot and few-shot prompting techniques
- Refine prompts iteratively to improve results

---

## Learning Outcomes

| # | Outcome |
|---|---------|
| 1 | Identify and write clear, effective prompts |
| 2 | Add context, goals, and constraints to guide LLMs |
| 3 | Use delimiters and request structured outputs |
| 4 | Demonstrate zero-shot and few-shot prompting |
| 5 | Practice iterative prompt refinement |

---

## Target Audience

Beginners and early learners in Generative AI, especially those new to prompt engineering.  
No prior experience with APIs or advanced NLP required.

---

## Prerequisites

- Completion of Day 03 (LLM basics, tokens, context windows, prompt-response flow)
- Basic Python or pseudocode reading skills (optional, not required for all exercises)
- No API keys or paid services needed

> **Instructor note:** This lab is concept-first and hands-on. It does not require real LLM API access. All exercises are designed for classroom discussion and practice.

---

## Lab Setup

1. No special software or environment is required.
2. Learners may use pen and paper, a text editor, or a Python REPL for practice.
3. All exercises can be completed offline.

---

## Lab Overview

```
Exercise 1  →  Weak vs strong prompts
Exercise 2  →  Add context and constraints
Exercise 3  →  Delimiters and output structure
Exercise 4  →  Zero-shot vs few-shot prompting
Exercise 5  →  Iterative refinement
```

**Estimated time:** 45–60 minutes  
**Format:** Instructor-led, hands-on, and discussion-based

---

## Exercise 1: Weak vs Strong Prompts

### Task

Suppose you want to summarize a short article. Compare the following prompts:

**Weak Prompt:**
```
Summarize this.

Artificial intelligence is transforming industries by automating tasks, improving decision-making, and enabling new products and services.
```

**Strong Prompt:**
```
You are a professional editor. Summarize the following paragraph in 2 sentences, using clear and neutral language, for a business audience.

Paragraph:
Artificial intelligence is transforming industries by automating tasks, improving decision-making, and enabling new products and services.
```

### Instructions
- Read both prompts.
- Discuss with a partner: Which prompt will likely produce a better summary? Why?
- Write your own improved version if possible.

### Expected Output
- The strong prompt will produce a more focused, concise, and relevant summary.
- The weak prompt may return a generic or incomplete answer.

> **Instructor note:** Emphasize the importance of role, audience, and format in prompt clarity.

---

## Exercise 2: Add Context and Constraints

### Task

Suppose you want an LLM to rewrite a technical explanation for a non-technical audience.

**Basic Prompt:**
```
Rewrite this for a general audience:

The TCP/IP protocol suite enables reliable data transmission across networks by using layered communication models and error-checking mechanisms.
```

**Improved Prompt with Context and Constraints:**
```
You are a technology writer. Rewrite the following explanation for a high school student with no technical background. Use simple language, keep it under 40 words, and avoid jargon.

Text:
The TCP/IP protocol suite enables reliable data transmission across networks by using layered communication models and error-checking mechanisms.
```

### Instructions
- Compare the two prompts.
- Identify what context (audience, goal) and constraints (length, language) were added.
- Try writing your own version for a different audience (e.g., business executive, child).

### Expected Output
- The improved prompt will yield a simpler, shorter, and more accessible explanation.
- Adding audience and constraints helps the LLM tailor its response.

> **Instructor note:** Encourage learners to experiment with different audiences and constraints.

---

## Exercise 3: Delimiters and Output Structure

### Task

Suppose you want a list of key points from a product review, formatted as bullet points.

**Prompt with Delimiters and Structure:**
```
Extract the main pros and cons from the following product review. List each as a bullet point under 'Pros' and 'Cons'.

Review:
---
I love the battery life and screen quality of this laptop, but the keyboard feels cramped and the fan is noisy.
---

Format:
Pros:
- ...
Cons:
- ...
```

### Instructions
- Note how the '---' delimiters clearly separate the review from the instructions.
- Observe how the requested output format is specified.
- Try writing a prompt that asks for a table or JSON output instead.

### Expected Output
- The LLM will return a structured list, e.g.:
```
Pros:
- battery life
- screen quality
Cons:
- keyboard feels cramped
- fan is noisy
```
- Using delimiters and explicit format requests increases output reliability.

> **Instructor note:** Show how delimiters reduce ambiguity and help with copy-paste or downstream processing.

---

## Exercise 4: Zero-Shot vs Few-Shot Prompting

### Task

Suppose you want to classify customer feedback as Positive, Negative, or Neutral.

**Zero-Shot Prompt:**
```
Classify the sentiment of this feedback as Positive, Negative, or Neutral:

"The app is easy to use, but sometimes crashes unexpectedly."
```

**Few-Shot Prompt:**
```
Classify the sentiment of each feedback as Positive, Negative, or Neutral.

Examples:
Feedback: "Great customer service and fast delivery."
Sentiment: Positive

Feedback: "The product did not work as advertised."
Sentiment: Negative

Feedback: "The app is easy to use, but sometimes crashes unexpectedly."
Sentiment:
```

### Instructions
- Compare the zero-shot and few-shot prompts.
- Discuss: Which is more likely to produce a consistent, accurate label? Why?
- Try adding your own example to the few-shot prompt.

### Expected Output
- The few-shot prompt will yield more consistent and accurate sentiment labels.
- Providing examples helps the LLM learn the pattern you want.

> **Instructor note:** Explain that few-shot prompting is especially useful for classification, extraction, and formatting tasks.

---

## Exercise 5: Iterative Refinement

### Task

Suppose your first prompt produces an incomplete or unsatisfactory answer. Practice improving it step by step.

**Round 1 Prompt:**
```
Explain blockchain.
```

**Round 1 Likely Output:**
```
Blockchain is a type of database that stores information in blocks that are linked together.
```

**Round 2 Improved Prompt:**
```
Explain blockchain to a high school student in 2 sentences, using a real-world analogy.
```

**Round 2 Likely Output:**
```
Blockchain is like a digital ledger where each page (block) records transactions and links to the previous page. This makes it very hard to change past records, ensuring security and trust.
```

**Round 3 Further Improved Prompt:**
```
You are a teacher. Explain blockchain to a high school student in 2 sentences, using a real-world analogy about keeping records in a classroom notebook.
```

**Round 3 Likely Output:**
```
Imagine a classroom notebook where each page records what happened each day, and every page is numbered and linked to the previous one. If someone tried to change an old page, everyone would notice, so the records stay trustworthy.
```

### Instructions
- Start with a basic prompt and review the answer.
- Revise the prompt to add audience, length, analogy, or context.
- Repeat for a third round, making the prompt even more specific.
- Note what changed and whether the answer improved.

### Expected Output
- Each round, the answer becomes clearer, more relevant, and better tailored to the audience.
- Iterative refinement is a key prompt engineering skill.

> **Instructor note:** Encourage learners to try their own iterative improvements on any topic.

---

## Key Observations

| Observation | Why it matters |
|-------------|---------------|
| Clear, specific prompts yield better outputs | LLMs need guidance to produce useful results |
| Adding context and constraints improves relevance | Audience, tone, and length shape the answer |
| Delimiters and format requests increase reliability | Structured outputs are easier to use and process |
| Few-shot prompts boost consistency | Examples help LLMs follow your pattern |
| Iterative refinement leads to better results | Prompt engineering is an interactive process |

---

## Troubleshooting Tips

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Output is too generic | Prompt is vague or lacks context | Add role, audience, or format details |
| Output ignores format | Did not specify structure or delimiters | Add explicit format instructions |
| LLM misses the task | Prompt is ambiguous | Clarify the task and add examples |
| Output is inconsistent | No examples provided | Use few-shot prompting |
| Still not satisfied | Prompt needs more refinement | Iterate and add more constraints |

---

## Summary / Recap

In this lab, you practiced the fundamentals of prompt engineering:
- Writing clear, specific prompts
- Adding context, constraints, and structure
- Using delimiters and requesting structured outputs
- Applying zero-shot and few-shot prompting
- Iteratively refining prompts for better results

**Key takeaway:** Prompt engineering is a practical, creative skill. The more you practice, the better your results will be. Every real-world LLM application depends on strong prompt design.

---

*Lab guide version: Day 04 — GenAI Foundation Training Program*  
*Estimated duration: 45–60 minutes*  
*No external APIs or API keys required*
