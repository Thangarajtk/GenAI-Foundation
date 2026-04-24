# Day 02 Lab Guide: Foundations of NLP and Transformers

## Objective
Understand basic text preprocessing, tokenization, context, and the intuition behind attention in NLP, using simple Python code.

## Learning Outcomes
- Distinguish between raw and cleaned text
- Apply basic text cleaning (lowercasing, punctuation, whitespace)
- Tokenize text and count tokens
- Observe how context changes word meaning
- Grasp the intuition behind attention (without math)
- Practice hands-on with your own text

## Prerequisites
- Basic Python knowledge (variables, functions, print)
- Python 3.x installed (no extra packages required)

## Setup Instructions
1. Open VS Code or Jupyter Notebook.
2. Download or copy `day02_demo.py` to your working folder.
3. (Optional) Use the notebook cells from `optional_jupyter_cells.md` for a step-by-step experience.

## Demo Overview
We will:
- Clean and tokenize sample text
- Count tokens
- See how context changes meaning
- Visualize "attention" by highlighting important words

## Step-by-Step Lab Tasks

### 1. Raw vs Cleaned Text
- Print a sample sentence as-is (raw)
- Clean it (lowercase, remove punctuation, trim spaces)
- Print the cleaned version

### 2. Tokenization
- Split cleaned text into tokens (words)
- Print the list of tokens

### 3. Token Counting
- Count the number of tokens
- Print the count

### 4. Context and Ambiguity
- Show how the word "bank" means different things in different sentences

### 5. Attention Intuition Demo
- Highlight important words in a sentence to show what "attention" means (no math)

## Hands-On Exercise

**Task:**  
Change the sample text in the script to your own sentence.  
- Clean and tokenize it.
- Observe how the tokens change.
- Try sentences with ambiguous words (e.g., "bat", "spring").

## Discussion Questions
1. Why is text cleaning important before tokenization?
2. How does context help us understand ambiguous words?
3. What might happen if we ignore punctuation or case in NLP tasks?

## Expected Observations
- Cleaned text is easier to process.
- Tokenization splits text into manageable pieces.
- The same word can have different meanings based on context.
- Highlighting important words helps us focus on meaning (attention intuition).

## Wrap-Up
- Text preprocessing is the first step in NLP.
- Tokenization and context are key for understanding language.
- Attention helps models (and humans) focus on what matters.

---

### Trainer Resources

**Suggested Questions:**
1. What changes do you notice after cleaning the text?
2. Can you think of other ambiguous words besides "bank"?
3. How would you decide which words are important in a sentence?

**Common Mistakes:**
1. Forgetting to lowercase text before tokenization.
2. Not removing punctuation, leading to tokens like "word,".
3. Using split() without cleaning whitespace, causing empty tokens.

**Troubleshooting Tips:**
1. If you see unexpected tokens, check if punctuation was removed.
2. If your token count is off, print the tokens list to debug.
3. If code errors, check for missing or extra parentheses/quotes.
