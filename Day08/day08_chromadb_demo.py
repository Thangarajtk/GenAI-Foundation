"""
Day 08 — Semantic Search with ChromaDB + OpenAI Embeddings
===========================================================
Run:  python day08_chromadb_demo.py

Prerequisites:
  pip install -r requirements.txt
  .env file in Day08/ with: OPENAI_API_KEY=sk-...

Demo structure
--------------
  section_1_setup()           — API key + clients
  section_2_database()        — ChromaDB persistent collection
  section_3_documents()       — define the FAQ knowledge base
  section_4_embed_and_store() — generate embeddings and upsert
  section_5_search()          — semantic similarity queries
  section_6_rag()             — retrieve → LLM grounded answer
  section_7_filters()         — metadata-filtered search
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

# ── Global handles (filled by section_1 and section_2) ──────────────────────
client     = None
collection = None

EMBED_MODEL     = "text-embedding-3-small"
CHAT_MODEL      = "gpt-4o-mini"
DB_PATH         = "./chroma_db"
COLLECTION_NAME = "support_faq"

SEPARATOR = "=" * 68


# ============================================================
#  SECTION 1 — Setup: API key + OpenAI client
# ============================================================
def section_1_setup():
    global client

    print(f"\n{SEPARATOR}")
    print("  SECTION 1 — Setup: API key + OpenAI client")
    print(SEPARATOR)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found.\n"
            "Create a .env file in Day08/ with:  OPENAI_API_KEY=sk-..."
        )

    client = OpenAI(api_key=api_key)

    print(f"  API key loaded : {api_key[:8]}...{api_key[-4:]}")
    print(f"  Embedding model: {EMBED_MODEL}")
    print(f"  Chat model     : {CHAT_MODEL}")


# ============================================================
#  SECTION 2 — Database: ChromaDB persistent collection
# ============================================================
def section_2_database():
    global collection

    print(f"\n{SEPARATOR}")
    print("  SECTION 2 — Database: ChromaDB persistent collection")
    print(SEPARATOR)

    # PersistentClient writes to disk — survives restarts
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}   # cosine similarity
    )

    print(f"  Storage path : {DB_PATH}")
    print(f"  Collection   : {COLLECTION_NAME}")
    print(f"  Docs stored  : {collection.count()}")


# ============================================================
#  SECTION 3 — Documents: define the FAQ knowledge base
# ============================================================
def section_3_documents() -> list:
    print(f"\n{SEPARATOR}")
    print("  SECTION 3 — Documents: IT support FAQ knowledge base")
    print(SEPARATOR)

    documents = [
        {
            "id":   "doc_01",
            "text": "To reset your password, go to the login page and click 'Forgot Password'. "
                    "You will receive a reset link by email within 5 minutes.",
            "metadata": {"category": "account",  "priority": "high"}
        },
        {
            "id":   "doc_02",
            "text": "VPN access is required when working from outside the office. "
                    "Download the company VPN client from the IT portal and use your Active Directory credentials.",
            "metadata": {"category": "network",  "priority": "high"}
        },
        {
            "id":   "doc_03",
            "text": "If your laptop is running slowly, try restarting it first. "
                    "If the problem persists, clear the browser cache or contact IT to check for malware.",
            "metadata": {"category": "hardware", "priority": "medium"}
        },
        {
            "id":   "doc_04",
            "text": "To request new software, submit a ticket in the IT portal under Software Requests. "
                    "Approval usually takes 2 business days.",
            "metadata": {"category": "software", "priority": "low"}
        },
        {
            "id":   "doc_05",
            "text": "Multi-factor authentication (MFA) is mandatory for all employees. "
                    "Install the Authenticator app and register your device via the security settings page.",
            "metadata": {"category": "security", "priority": "high"}
        },
        {
            "id":   "doc_06",
            "text": "Your work email is hosted on Microsoft 365. "
                    "Access it at mail.company.com or via Outlook desktop.",
            "metadata": {"category": "email",    "priority": "low"}
        },
        {
            "id":   "doc_07",
            "text": "To share files with external partners, use the approved SharePoint folder. "
                    "Do not use personal cloud storage such as Dropbox or Google Drive for company data.",
            "metadata": {"category": "security", "priority": "high"}
        },
        {
            "id":   "doc_08",
            "text": "If you cannot connect to Wi-Fi, ensure your device is in range and that the SSID is "
                    "'CorpNet-Secure'. Restart your network adapter or contact IT if the issue continues.",
            "metadata": {"category": "network",  "priority": "medium"}
        },
        {
            "id":   "doc_09",
            "text": "Printers on the office network can be added through Settings > Printers & Scanners. "
                    "Search for the printer by name (e.g., 'FloorPrinter-3A') and install the driver automatically.",
            "metadata": {"category": "hardware", "priority": "low"}
        },
        {
            "id":   "doc_10",
            "text": "Software licenses are tracked centrally. If your license expires, submit a renewal request "
                    "in the IT portal at least 5 business days before expiry.",
            "metadata": {"category": "software", "priority": "medium"}
        },
    ]

    print(f"  {len(documents)} documents defined.\n")
    for doc in documents:
        print(f"  [{doc['id']}] ({doc['metadata']['category']:8s})  {doc['text'][:60]}...")

    return documents


# ============================================================
#  SECTION 4 — Embed & Store: generate embeddings and upsert
# ============================================================
def _get_embeddings(texts: list) -> list:
    """Call OpenAI Embeddings API; return list of float vectors."""
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]


def section_4_embed_and_store(documents: list):
    print(f"\n{SEPARATOR}")
    print("  SECTION 4 — Embed & Store: OpenAI embeddings → ChromaDB")
    print(SEPARATOR)

    # Skip documents already in the collection (safe for reruns)
    existing_ids = set(collection.get()["ids"])
    new_docs     = [d for d in documents if d["id"] not in existing_ids]

    if new_docs:
        texts      = [d["text"]     for d in new_docs]
        ids        = [d["id"]       for d in new_docs]
        metadatas  = [d["metadata"] for d in new_docs]

        print(f"  Generating embeddings for {len(new_docs)} document(s)...")
        embeddings = _get_embeddings(texts)

        print(f"  Vector dimensions : {len(embeddings[0])}")
        print(f"  First 5 values    : {[round(v, 6) for v in embeddings[0][:5]]}")

        collection.add(
            ids=ids, documents=texts,
            embeddings=embeddings, metadatas=metadatas
        )
        print(f"  Stored {len(new_docs)} new document(s).")
    else:
        print("  All documents already in collection — nothing to add.")

    print(f"  Total in collection: {collection.count()}")


# ============================================================
#  SECTION 5 — Search: semantic similarity queries
# ============================================================
def _search(query: str, top_k: int = 3) -> dict:
    """Embed the query and return top-k closest documents."""
    query_vec = _get_embeddings([query])[0]
    return collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )


def section_5_search():
    print(f"\n{SEPARATOR}")
    print("  SECTION 5 — Search: semantic similarity queries")
    print(SEPARATOR)

    # ── 5a: single query, top-3 ranked results ───────────────
    query = "How do I connect to the office VPN from home?"
    print(f"\n  Query: \"{query}\"\n")

    results = _search(query, top_k=3)
    print(f"  {'Rank':<4} {'ID':<8} {'Distance':>9}  {'Category':<10}  Document")
    print("  " + "-" * 72)
    for rank, (doc_id, doc, meta, dist) in enumerate(
        zip(results["ids"][0], results["documents"][0],
            results["metadatas"][0], results["distances"][0]),
        start=1
    ):
        print(f"  {rank:<4} {doc_id:<8} {dist:>9.4f}  {meta['category']:<10}  {doc[:55]}...")

    # ── 5b: batch queries to observe similarity behaviour ────
    sample_queries = [
        "My computer is really slow today",
        "I forgot my login credentials",
        "How do I print a document?",
        "What is the company email system?",
    ]
    print(f"\n  Batch queries — top-1 match each:\n")
    for q in sample_queries:
        res  = _search(q, top_k=1)
        doc  = res["documents"][0][0]
        dist = res["distances"][0][0]
        pid  = res["ids"][0][0]
        print(f"  Q: {q}")
        print(f"     [{pid}] dist={dist:.4f}  {doc[:65]}...")
        print()

    print("  Distance guide: ~0.0 identical  |  <0.3 very similar  |  >0.6 unrelated")


# ============================================================
#  SECTION 6 — RAG: retrieve → LLM grounded answer
# ============================================================
def _rag_answer(question: str, top_k: int = 3) -> str:
    """
    Retrieval-Augmented Generation (RAG):
      1. Embed the question → retrieve top-k docs from ChromaDB.
      2. Inject retrieved docs as context into the LLM prompt.
      3. LLM answers from context only — no hallucination.
    """
    results = _search(question, top_k=top_k)
    context = "\n".join(
        f"[Doc {i+1}] {doc}"
        for i, doc in enumerate(results["documents"][0])
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an IT support assistant. "
                    "Answer using ONLY the context below. "
                    "If the answer is not there, say you don't have enough information."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.2,
        max_tokens=300
    )
    return response.choices[0].message.content


def section_6_rag():
    print(f"\n{SEPARATOR}")
    print("  SECTION 6 — RAG: retrieve context → LLM grounded answer")
    print(SEPARATOR)
    print("  Pattern:  question → embed → ChromaDB → top docs → LLM → answer\n")

    questions = [
        ("in-scope  ", "How do I connect to the VPN from home?"),
        ("in-scope  ", "My laptop is running slowly. What should I do?"),
        ("OUT-of-scope", "What is the company holiday schedule for this year?"),
    ]

    for label, q in questions:
        print(f"  [{label}] Q: {q}")
        print(f"  {'-'*64}")
        print(f"  {_rag_answer(q)}")
        print()


# ============================================================
#  SECTION 7 — Filters: metadata-filtered search
# ============================================================
def _search_filtered(query: str, category: str, top_k: int = 3) -> dict:
    """Search only within documents that match a metadata category."""
    query_vec = _get_embeddings([query])[0]
    return collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        where={"category": category},
        include=["documents", "metadatas", "distances"]
    )


def section_7_filters():
    print(f"\n{SEPARATOR}")
    print("  SECTION 7 — Filters: metadata-filtered search")
    print(SEPARATOR)

    query = "How should I handle company files?"
    print(f"  Query: \"{query}\"\n")

    for category in ("security", "network", "hardware"):
        res = _search_filtered(query, category=category, top_k=1)
        if res["documents"][0]:
            doc  = res["documents"][0][0]
            dist = res["distances"][0][0]
            print(f"  Filter [{category:8s}]  dist={dist:.4f}  {doc[:65]}...")
        else:
            print(f"  Filter [{category:8s}]  no results")

    print(f"\n  TIP: filter by priority='high' to surface urgent policies only.")


# ============================================================
#  MAIN — run all sections in order
# ============================================================
def main():
    print(f"\n{'#'*68}")
    print("#  Day 08 — ChromaDB + OpenAI Semantic Search Demo")
    print(f"{'#'*68}")

    section_1_setup()
    section_2_database()
    documents = section_3_documents()
    section_4_embed_and_store(documents)
    section_5_search()
    section_6_rag()
    section_7_filters()

    print(f"\n{SEPARATOR}")
    print("  Demo complete.")
    print(f"  Data persisted in: {DB_PATH}/")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
