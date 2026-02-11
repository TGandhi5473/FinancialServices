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
cd financialservices
pip install -r requirements.txt
python sync_tickers.py
```
## 📂 Project Structure

| File / Folder | Description |
| :--- | :--- |
| `app.py` | Main Streamlit interface and session state controller. |
| `src/judge.py` | Dual-agent reasoning logic (Analyst + Auditor). |
| `src/scraper.py` | Deterministic SEC EDGAR data extraction via `edgartools`. |
| `src/ingester.py` | Local Vector DB management using `ChromaDB`. |
| `src/evaluator.py` | JSONL log parsing and metric calculations. |
| `data/us_tickers.csv` | **(Included)** Pre-cached mapping of 10,000+ US Tickers. |
| `logs/` | **(Ignored)** Local JSONL audit trails for reasoning history. |
| `vector_db/` | **(Ignored)** Persistent embeddings for indexed filings. |

## 🔒 Privacy & Security

- **No Data Leaks:** Raw filings, logs, and vector stores are excluded from Git via `.gitignore`. Your research history stays on your machine.
- **Credential Safety:** API keys and emails are handled via Streamlit session state and are never hardcoded or saved to disk.
- **Auditability:** The local log system ensures you can always trace how the AI arrived at a specific financial conclusion by comparing the Analyst's draft vs. the Auditor's refinement.

- ## 🖥️ Usage

1. **Launch the App:**
2. Setup Identity: Enter your email in the sidebar (required for SEC EDGAR compliance).
3. Ingest Data: Search for a company. If it's your first time analyzing them, the app will scrape and index the 10-K.
4. Audit: Enable High Precision Mode to trigger the Senior Auditor agent for verified results.
   ```bash
   streamlit run app.py
