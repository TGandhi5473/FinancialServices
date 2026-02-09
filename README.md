# 🛡️ Fin-Agent Local: Autonomous SEC Analyst

**Fin-Agent Local** is a "Bring Your Own Key" (BYOK) and "Bring Your Own Identity" (BYOI) research tool. It automates the extraction of SEC 10-K and 10-Q filings, builds a local knowledge base, and uses an agentic reasoning loop to perform deep financial audits.



---

## 🚀 The Philosophy
This tool utilizes a **Hybrid Architecture** to ensure financial accuracy:
1.  **Deterministic Extraction:** Python scripts via `edgartools` handle the "Facts" (SEC filings, XBRL data) to prevent math hallucinations.
2.  **Probabilistic Reasoning:** Local (Ollama) or Cloud (OpenAI) agents handle the "Judgment" (analyzing management tone, risk factors, and environmental shifts).

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Python 3.10+**
* **Ollama:** [Download here](https://ollama.com/)
    * `ollama pull deepseek-r1:7b` (Recommended Reasoning Model)
    * `ollama pull nomic-embed-text` (Required Embedding Model)

### 2. Clone & Install
```bash
git clone [https://github.com/TGandhi5473/FinancialServices.git]
cd FinancialServices
pip install -r requirements.txt

3. Initialize Ticker Database
This repo includes a pre-loaded data/us_tickers.csv. To update it to the absolute latest SEC mapping (recommended monthly):
Bashpython sync_tickers.py
🖥️ UsageRun the Streamlit interface:
Bash
streamlit run app.py
The Workflow:Identity: Enter your email in the sidebar (Required by SEC EDGAR compliance).Selection: Search for any US-listed company via the autocomplete search.Ingestion: If the data isn't cached, the script will fetch the 10-K and index it locally.
Analysis: Query the "Judge" to analyze the filing using either your local GPU or an OpenAI API key.
📂 Project Structure
File/FolderPurposeapp.py
The Streamlit entry point and "Gatekeeper" logic.
src/scraper.py
Handles deterministic extraction from SEC EDGAR.
src/ingester.py
Manages local RAG (Vector DB) creation.
src/judge.pyThe Agentic loop that switches between Local and Cloud LLMs.vector_db/(Ignored) Local binary storage for indexed filings.data/filings/(Ignored) Cached raw text and JSON from the SEC.data/us_tickers.csv(Included) Pre-loaded list of 10k+ US tickers for fast lookup.
🔒 Security & Privacy
Local First: Filings and Vector indices are stored on your machine. The .gitignore prevents accidental leaks of private financial data to GitHub.
BYO Credentials: No API keys or emails are hardcoded. Your email is only used for the User-Agent header as per SEC requirements.Compliance: The application strictly adheres to the SEC's 10-request-per-second limit.
⚖️ LicenseDistributed under the MIT License. See LICENSE for more information.
