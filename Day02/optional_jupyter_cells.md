# Day 02 NLP Lab: Notebook Cells

Below are notebook-friendly cells for the Day 02 demo.  
Copy each cell into your Jupyter Notebook or VS Code interactive window.

---

**Cell 1: Introduction**

```python
# Day 02 NLP Lab: Text Preprocessing and Attention Intuition
# This notebook will guide you through basic NLP steps using simple Python code.
```

---

**Cell 2: Sample Text and Cleaning Function**

```python
import string

# Sample multiline text block
SAMPLE_TEXT = """
  The Bank of the river was steep.
  I went to the bank to deposit money.
  Let's sit on the river bank and watch the sunset!
"""

def clean_text(text):
    """
    Lowercase, remove punctuation, and trim extra whitespace.
    """
    print("Raw text:")
    print(text)
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove extra whitespace
    text = ' '.join(text.split())
    print("\nCleaned text:")
    print(text)
    return text
```

---

**Cell 3: Tokenization Function**

```python
def tokenize_text(text):
    """
    Split text into tokens (words).
    """
    tokens = text.split()
    print("\nTokens:")
    print(tokens)
    return tokens
```

---

**Cell 4: Token Counting Function**

```python
def count_tokens(tokens):
    """
    Count the number of tokens.
    """
    count = len(tokens)
    print(f"\nNumber of tokens: {count}")
    return count
```

---

**Cell 5: Clean and Tokenize Sample Text**

```python
# Clean and tokenize the sample text
cleaned = clean_text(SAMPLE_TEXT)
tokens = tokenize_text(cleaned)
count_tokens(tokens)
```

---

**Cell 6: Context Meaning Example**

```python
def compare_context_examples():
    """
    Show how 'bank' changes meaning based on context.
    """
    examples = [
        "The Bank of the river was steep.",
        "I went to the bank to deposit money.",
        "Let's sit on the river bank and watch the sunset!"
    ]
    print("\nContext Meaning Demo:")
    for i, sentence in enumerate(examples, 1):
        print(f"Example {i}: {sentence}")
    print("\nNotice how 'bank' refers to a river's edge in some sentences, and a financial institution in another.")

compare_context_examples()
```

---

**Cell 7: Attention Intuition Demo**

```python
def attention_intuition_demo():
    """
    Highlight important words in a sentence (attention intuition).
    """
    sentence = "The quick brown fox jumps over the lazy dog."
    important_words = ["fox", "jumps", "dog"]
    print("\nAttention Intuition Demo:")
    print("Original sentence:")
    print(sentence)
    print("Highlighting important words (like attention):")
    highlighted = []
    for word in sentence.split():
        if word.strip(string.punctuation).lower() in important_words:
            highlighted.append(f"[{word.upper()}]")
        else:
            highlighted.append(word)
    print(' '.join(highlighted))
    print("\nThis shows how attention helps focus on key words.")

attention_intuition_demo()
```

---

**Cell 8: Hands-On Exercise**

```python
# Hands-On: Try your own sentence!
user_text = "The bat flew at night. He swung the bat at the ball."
print(f"\nYour sample text:\n{user_text}")
cleaned_user = clean_text(user_text)
tokens_user = tokenize_text(cleaned_user)
count_tokens(tokens_user)

# Try changing 'user_text' to your own sentence and rerun this cell!
```

---

**Cell 9: Discussion**

```markdown
## Discussion

- Why is text cleaning important before tokenization?
- How does context help us understand ambiguous words?
- What might happen if we ignore punctuation or case in NLP tasks?
```
