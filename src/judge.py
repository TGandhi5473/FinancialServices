import os
import json
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.schema import SystemMessage, HumanMessage

def log_audit(ticker, query, analyst_draft, final_verdict, mode):
    """Saves the reasoning process to a local JSONL file for evaluation."""
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ticker": ticker,
        "query": query,
        "model": mode,
        "analyst_draft": analyst_draft,
        "final_verdict": final_verdict,
        # A simple heuristic to see if the Auditor actually changed anything
        "was_refined": analyst_draft.strip() != final_verdict.strip()
    }
    
    with open("logs/audit_trail.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def run_local_judge(ticker, query, mode="Local", api_key=None, high_precision=True):
    # 1. Initialize LLM
    if mode == "OpenAI" and api_key:
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0.1)
    else:
        llm = ChatOllama(model="deepseek-r1:7b", temperature=0.1)

    # 2. Retrieve Context
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db_path = f"vector_db/{ticker}"
    
    if not os.path.exists(db_path):
        return "Error: Local knowledge base not found."
        
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    docs = db.similarity_search(query, k=5)
    context_text = "\n---\n".join([d.page_content for d in docs])

    # --- STEP 1: PRIMARY ANALYST PASS ---
    analyst_system = f"You are a Junior Financial Analyst for {ticker}. Use ONLY the context provided."
    analyst_query = f"CONTEXT:\n{context_text}\n\nUSER QUERY: {query}"
    
    analyst_output = llm.invoke([
        SystemMessage(content=analyst_system),
        HumanMessage(content=analyst_query)
    ]).content

    if not high_precision:
        return analyst_output

    # --- STEP 2: SENIOR AUDITOR PASS ---
    

    auditor_system = f"""
    You are a Senior Auditor. Review the Analyst's report for {ticker}.
    Cross-reference every claim against the SOURCE CONTEXT.
    Source: {context_text}
    Analyst Draft: {analyst_output}
    """
    
    final_output = llm.invoke([
        SystemMessage(content=auditor_system),
        HumanMessage(content="Perform final audit. Correct errors or finalize.")
    ]).content

    # 3. Log the process for progress tracking
    log_audit(ticker, query, analyst_output, final_output, mode)
    
    return final_output
