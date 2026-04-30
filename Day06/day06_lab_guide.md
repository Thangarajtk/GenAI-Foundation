# Day 06 Lab Guide: Text Generation & Chatbots

---

## Objective

Build a working IT Help Desk chatbot that maintains conversation history, uses a system prompt to control behavior, streams responses, and handles errors gracefully.

---

## Prerequisites

- Day 05 environment working (OpenAI API key in `.env`, `openai` and `python-dotenv` installed)
- Python 3.8+
- VS Code or Jupyter Notebook

---

## Setup

```bash
cd Day06
cp .env.example .env        # add your OPENAI_API_KEY
pip install -r requirements.txt
```

Run the demo to verify your environment before starting the exercises:

```bash
python day06_demo.py
```

---

## Exercises

---

### Exercise 1: Send Your First Message

**Objective:** Call the OpenAI Chat Completions API with a single user message and print the response.

**Tasks:**
- Create a new Python file `chatbot.py`
- Initialize the OpenAI client using your API key from `.env`
- Define a system prompt that introduces the chatbot (e.g., an IT Help Desk assistant)
- Send one user message and print the response

**Expected behavior:** The model replies with a relevant, on-topic response matching the system prompt persona.

**Validation:** Response prints to the console without errors.

---

### Exercise 2: Maintain Conversation History

**Objective:** Verify the model retains context across multiple turns.

**Tasks:**
- Extend `chatbot.py` to store all messages in a list (system + user + assistant)
- Send at least 3 follow-up messages in sequence
- After each turn, print the full messages list to inspect its state

**Example sequence to try:**
1. "How do I reset my password?"
2. "What if I don't have access to my recovery email?"
3. "Can I do this on my phone?"

**Expected behavior:** The model's later answers reference context from earlier in the conversation.

**Validation:** The messages list grows by 2 entries per turn (one user, one assistant).

---

### Exercise 3: Customize the System Prompt

**Objective:** Change the chatbot's persona and observe how response style shifts.

**Tasks:**
- Try each of the following system prompts and send the same user message each time
- Note how tone, scope, and style differ

**Prompts to try:**

```
You are a friendly FAQ bot for a software company. Answer only product-related questions. Be brief and use bullet points.
```

```
You are a formal enterprise support agent. Use professional language and always end with "Is there anything else I can help you with?"
```

```
You are an email drafting assistant. Rewrite the user's request as a polished, professional email reply.
```

**Expected behavior:** The same user question produces noticeably different responses for each system prompt.

**Validation:** Run all three and compare outputs side by side.

---

### Exercise 4: Enable Streaming Output

**Objective:** Print response tokens as they arrive instead of waiting for the full reply.

**Tasks:**
- Update your API call to use `stream=True`
- Iterate over the streamed chunks and print each token as it arrives
- Collect the full response and append it to chat history when streaming is complete

**Key pattern:**
```python
stream = client.chat.completions.create(..., stream=True)
for chunk in stream:
    token = chunk.choices[0].delta.content
    if token:
        print(token, end="", flush=True)
```

**Expected behavior:** Text appears incrementally in the console, word by word.

**Validation:** The response prints gradually rather than all at once. Chat history still contains the complete message after the loop ends.

---

### Exercise 5: Add Basic Error Handling

**Objective:** Catch and handle API errors gracefully without crashing the program.

**Tasks:**
- Wrap your API call in a `try/except` block
- Handle at minimum: `AuthenticationError`, `RateLimitError`, and a general `Exception` fallback
- Print a user-friendly message for each error type

**Validation:** Test by temporarily setting `OPENAI_API_KEY=invalid` in your `.env` and confirming the error is caught and reported cleanly instead of raising a traceback.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `API key not found` | Check `.env` exists and `load_dotenv()` is called before `os.getenv()` |
| `AuthenticationError` | API key is invalid or has expired |
| `openai.Completion` removed error | You are on `openai>=1.0.0` — use `client.chat.completions.create()` |
| Streaming prints nothing | Check `if token:` guard — `delta.content` can be `None` for the first/last chunk |
| Model ignores earlier context | Ensure you pass the full `messages` list (not just the latest message) on every call |
| Rate limit hit | Add `time.sleep(1)` between rapid calls in a loop |

---

## Reference: Folder Structure

```
Day06/
├── .env                   # your API key (never commit this)
├── .env.example
├── requirements.txt
├── day06_demo.py          # trainer demo — reference implementation
├── day06_demo.ipynb       # notebook version
└── chatbot.py             # your hands-on exercise file
```

---

*Lab guide version: Day 06 — GenAI Foundation Training Program*  
*Estimated duration: 60–90 minutes*
