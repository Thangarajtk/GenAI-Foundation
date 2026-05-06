# Day 08 Lab Guide — Semantic Search with ChromaDB + OpenAI Embeddings

---

## Objective

By the end of this lab you will be able to:

- Generate text embeddings using the OpenAI `text-embedding-3-small` model.
- Store and retrieve those embeddings in a local ChromaDB vector database.
- Understand how cosine distance reflects semantic similarity.
- Build a simple RAG (Retrieval-Augmented Generation) pipeline: embed → search → LLM answer.

---

## Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.8 or higher |
| OpenAI API key | Same key used in Day 05 / 06 / 07 |
| Virtual environment | `.venv` in the project root (already set up) |
| Day 05 environment | `openai` and `python-dotenv` must be installed |

---

## Environment Setup

```bash
# 1. Navigate to the Day08 folder
cd Day08

# 2. Activate the shared virtual environment
source ../.venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate            # Windows

# 3. Install Day 08 dependencies
pip install -r requirements.txt

# 4. Create your .env file with your OpenAI key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

> **Note:** The `chroma_db/` folder will be created automatically when you first run the notebook. Do not delete it between sessions — it holds your stored embeddings.

---

## How to Open the Demo Notebook

```bash
# Option A — VS Code
code day08_chromadb_demo.ipynb

# Option B — Jupyter
jupyter notebook day08_chromadb_demo.ipynb
```

Run each cell **top to bottom** before starting the exercises below.

---

## Lab Exercises

---

### Exercise 1 — Verify the Setup

**Objective:** Confirm that ChromaDB and the OpenAI client are configured correctly.

**Tasks:**

1. Open `day08_chromadb_demo.ipynb`.
2. Run **Step 1** (install) and **Step 2** (imports + API key).
3. Verify the output shows:
   - Your API key prefix (e.g., `sk-proj-...`).
   - Embedding model: `text-embedding-3-small`.
   - Chat model: `gpt-4o-mini`.

**Expected output:**

```
API key loaded: sk-proj-...xxxx
Embedding model : text-embedding-3-small
Chat model      : gpt-4o-mini
```

**Validation:** No `EnvironmentError` is raised. The key prefix is printed without exposing the full key.

---

### Exercise 2 — Initialise the Collection

**Objective:** Create a persistent ChromaDB collection.

**Tasks:**

1. Run **Step 3** of the notebook.
2. Observe the confirmation message.
3. Check that a `chroma_db/` folder was created in `Day08/`.

**Expected output (first run):**

```
Collection 'support_faq' ready. Documents currently stored: 0
```

**Expected output (subsequent runs):**

```
Collection 'support_faq' ready. Documents currently stored: 10
```

**Validation:** The `chroma_db/` folder appears in the file explorer.

---

### Exercise 3 — Add Your Own Documents

**Objective:** Extend the document set with your own entries.

**Tasks:**

1. After Step 4 in the notebook (but before Step 6), add the following code block:

```python
custom_documents = [
    {
        "id": "doc_11",
        "text": "To book a meeting room, use the Room Booking system on the intranet. "
                "Rooms can be reserved up to 4 weeks in advance.",
        "metadata": {"category": "facilities", "priority": "low"}
    },
    {
        "id": "doc_12",
        "text": "If you receive a suspicious email, do not click any links. "
                "Forward it to security@company.com immediately.",
        "metadata": {"category": "security", "priority": "high"}
    },
]
documents.extend(custom_documents)
print(f"Document list now has {len(documents)} entries.")
```

2. Re-run Steps 5 and 6 (generate embeddings, add to collection).
3. Verify the collection now contains 12 documents.

**Expected output:**

```
Added 2 new document(s).
Total documents in collection: 12
```

**What to observe:** Only the two new documents are embedded and added; the existing 10 are skipped because of the `existing_ids` check.

---

### Exercise 4 — Run Semantic Queries

**Objective:** Observe how the search returns semantically related documents even when exact keywords do not match.

**Tasks:**

Run the following queries one at a time and note the top result and its distance:

```python
queries = [
    "I can't log in to my account",
    "How do I install new software on my work laptop?",
    "I got a phishing email",
    "I need to print from my computer",
    "How do I share files with someone outside the company?",
]

for q in queries:
    res = search(q, top_k=1)
    doc  = res["documents"][0][0]
    dist = res["distances"][0][0]
    pid  = res["ids"][0][0]
    print(f"Q: {q}")
    print(f"   Match [{pid}] dist={dist:.4f}: {doc[:80]}...")
    print()
```

**What to observe:**

- `"I can't log in"` should match `doc_01` (password reset), not an exact keyword match.
- `"phishing email"` should match one of the security documents.
- Distances below `0.4` generally indicate a good semantic match.

**Validation:** At least 4 out of 5 queries return a relevant document (distance < 0.5).

---

### Exercise 5 — Explore Embedding Dimensions

**Objective:** Inspect the raw embedding vector to build intuition.

**Tasks:**

Add and run this code:

```python
text_a = "How do I reset my password?"
text_b = "I forgot my login credentials"
text_c = "What is the company holiday schedule?"

vecs = get_embeddings([text_a, text_b, text_c])

import math

def cosine_similarity(a, b):
    dot   = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(x**2 for x in b))
    return dot / (mag_a * mag_b)

sim_ab = cosine_similarity(vecs[0], vecs[1])
sim_ac = cosine_similarity(vecs[0], vecs[2])

print(f"Similarity (password vs login credentials): {sim_ab:.4f}")
print(f"Similarity (password vs holiday schedule) : {sim_ac:.4f}")
print(f"\nConclusion: score closer to 1.0 = more similar")
```

**Expected output (approximate):**

```
Similarity (password vs login credentials): 0.87 – 0.93
Similarity (password vs holiday schedule) : 0.50 – 0.65
```

**What to observe:** Semantically related sentences score much higher even though they use different words.

---

### Exercise 6 — RAG: Search + LLM Answer

**Objective:** Use the retrieved context to generate a grounded answer.

**Tasks:**

1. Run **Steps 8–10** of the notebook.
2. Then ask a question that is **not** in the knowledge base:

```python
question = "Can I use personal Dropbox for work files?"
print(rag_answer(question))
```

3. Ask a question that is **completely outside** the knowledge base:

```python
question = "What is the weather like in London today?"
print(rag_answer(question))
```

**What to observe:**

- For the Dropbox question: the LLM finds `doc_07` (file sharing policy) and gives a grounded answer.
- For the weather question: the LLM says it does not have enough information — this is the correct, safe behaviour.

**Validation:** The LLM does **not** hallucinate an answer for the out-of-scope question.

---

### Exercise 7 — Metadata Filtering

**Objective:** Restrict search to a subset of documents using metadata.

**Tasks:**

Run the `search_filtered` function (Step 9 of the notebook) for each category:

```python
categories = ["account", "network", "hardware", "security", "software", "email"]

q = "I need help with my work setup"
for cat in categories:
    try:
        res = search_filtered(q, category=cat, top_k=1)
        doc  = res["documents"][0][0]
        dist = res["distances"][0][0]
        print(f"[{cat:10s}] dist={dist:.4f}  {doc[:70]}...")
    except Exception as e:
        print(f"[{cat:10s}] No documents in this category or error: {e}")
```

**What to observe:** The same query returns a different best match depending on which category filter is applied.

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `EnvironmentError: OPENAI_API_KEY not found` | `.env` file missing or key name wrong | Create `Day08/.env` with `OPENAI_API_KEY=sk-...` |
| `ModuleNotFoundError: No module named 'chromadb'` | Package not installed | Run `pip install -r requirements.txt` |
| `chromadb.errors.UniqueConstraintError` | Adding a document ID that already exists | The notebook's `existing_ids` check prevents this; ensure you use it |
| `openai.AuthenticationError` | Invalid or expired API key | Check key at platform.openai.com → API Keys |
| `openai.RateLimitError` | Too many requests in a short window | Wait 30 seconds and retry; reduce batch size |
| `collection.query` returns fewer results than `n_results` | Collection has fewer documents than `top_k` | Normal behaviour; reduce `top_k` or add more documents |
| `chroma_db/` folder missing after restart | Notebook was run without write permission | Ensure you have write access to `Day08/`; run from that directory |

---

## Validation Checklist

Before finishing, confirm each item:

- [ ] `.env` file exists in `Day08/` with a valid `OPENAI_API_KEY`.
- [ ] `pip install -r requirements.txt` completed without errors.
- [ ] Notebook Steps 1–10 ran without exceptions.
- [ ] `chroma_db/` folder exists and contains data.
- [ ] At least 10 documents are stored in the collection.
- [ ] A semantic query returns a relevant result with distance < 0.5.
- [ ] The RAG function answers a grounded question correctly.
- [ ] The RAG function refuses to answer an out-of-scope question.
- [ ] You added at least 1 custom document and queried it successfully.

---

## Key Concepts Recap

| Concept | One-line explanation |
|---|---|
| **Embedding** | A list of numbers that represents the meaning of a text |
| **Cosine distance** | Measures how different two vectors are; 0 = identical, 1 = opposite |
| **Vector database** | A database optimised for storing and searching embeddings |
| **ChromaDB** | An open-source, local vector database; no cloud account needed |
| **RAG** | Retrieve relevant documents first, then pass them to the LLM as context |
| **Metadata filter** | Narrow a vector search to a subset of documents before ranking by similarity |
