# 🛡️ Fin-Agent Local: High-Precision SEC Auditor

**Fin-Agent Local** is a "Bring Your Own Key" (BYOK) and "Bring Your Own Identity" (BYOI) research workbench. It automates the extraction of SEC 10-K filings, builds a local RAG knowledge base, and utilizes a **Dual-Agent Audit** loop to ensure financial analysis is grounded and hallucination-free.



---

## 🚀 Key Features
- **Dual-Agent Reasoning:** Features a *Junior Analyst* pass followed by a *Senior Auditor* verification pass.
- **Local RAG:** Uses `ChromaDB` and `nomic-embed-text` to keep your financial data on your machine.
- **Audit Trails:** Automatically logs every draft and final verdict to `logs/audit_trail.jsonl` for performance tracking.
- **SEC Compliance:** Built-in identity gating to comply with SEC EDGAR's automated access policies.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **Ollama:** [Download here](https://ollama.com/)
    - `ollama pull deepseek-r1:7b` (Recommended Reasoning Model)
    - `ollama pull nomic-embed-text` (Required Embedding Model)

### 2. Installation
```bash
git clone [https://github.com/TGandhi5473/financialservices.git](https://github.com/TGandhi5473/financialservices.git)
cd FinancialServices
pip install -r requirements.txt
python sync_tickers.py


🖥️ Usage
Launch the App:

Bash

streamlit run app.py
Setup Identity: Enter your email in the sidebar (required for SEC data access).

Ingest Data: Select a company (e.g., AAPL, NVDA). If the local index doesn't exist, the app will scrape and embed the latest 10-K automatically.

Audit: Ask complex questions. Enable High Precision Mode to see the Auditor agent refine the Analyst's initial findings.

Analyze Logs: Expand the "Audit History" in the sidebar to view the "Before vs. After" of your agentic reasoning.


File,Description
app.py,Streamlit UI with integrated Log Viewer.
src/judge.py,Core Agentic logic (Analyst + Auditor).
src/scraper.py,Deterministic SEC EDGAR data extraction.
src/ingester.py,Local Vector DB management (Chroma).
src/evaluator.py,Log parsing and metrics calculation.
logs/,(Ignored) Local JSONL audit trails.
vector_db/,(Ignored) Local persistent embeddings.


🔒 Privacy & Security
No Data Leaks: Raw filings and vector stores are excluded from Git via .gitignore.

Credential Safety: API keys and emails are handled via session state and never hardcoded.

Auditability: The local log system ensures you can always trace how the AI arrived at a specific financial conclusion.

⚖️ License
Distributed under the MIT License.
