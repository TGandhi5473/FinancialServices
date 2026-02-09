import streamlit as st
import pandas as pd
import os
from src.scraper import collect_financials
from src.ingester import create_vector_store
from src.judge import run_local_judge
from sync_tickers import sync_sec_tickers # Import the sync function

st.set_page_config(page_title="Fin-Agent Local", layout="wide")

# Sidebar: BYO-Identity and BYO-Key
with st.sidebar:
    st.header("🔑 Auth & Identity")
    user_email = st.text_input("SEC User-Agent Email", placeholder="analyst@firm.com")
    st.divider()
    engine = st.radio("Inference Engine", ["Local (Free)", "OpenAI (Key Required)"])
    api_key = st.text_input("OpenAI Key", type="password") if engine == "OpenAI (Key Required)" else None

st.title("🛡️ Fin-Agent Judge")

# 1. Ticker List Management (The "Pre-Loaded" Logic)
TICKER_PATH = "data/us_tickers.csv"

if not os.path.exists(TICKER_PATH):
    st.warning("Ticker list not found locally.")
    if st.button("Sync Ticker List (One-time)"):
        with st.spinner("Fetching SEC ticker mapping..."):
            sync_sec_tickers()
            st.rerun()
    st.stop() # Don't run the rest of the app until list exists

@st.cache_data
def load_tickers():
    return pd.read_csv(TICKER_PATH)['Symbol'].tolist()

ticker_list = load_tickers()
ticker = st.selectbox("Search US Tickers", options=ticker_list, index=None)

# 2. Gatekeeper Logic
if ticker:
    if not user_email:
        st.warning("Please enter your email in the sidebar to enable SEC data retrieval.")
    else:
        db_path = f"vector_db/{ticker}"
        
        # Check if we already have the analysis ready
        if not os.path.exists(db_path):
            st.info(f"No local data for {ticker}. The Judge needs to ingest the latest filings.")
            if st.button(f"Scrape & Index {ticker}"):
                with st.status(f"Ingesting {ticker}...") as status:
                    st.write("Fetching 10-K and Facts from EDGAR...")
                    path = collect_financials(ticker, user_email)
                    st.write("Building Local Vector Index...")
                    create_vector_store(path, ticker)
                    status.update(label="Index Built!", state="complete")
                st.rerun()
        else:
            st.success(f"✅ Analysis environment for {ticker} is ready.")
            query = st.text_area("Analyze specific risk or factor:", "Provide a verdict on the company's solvency and environmental risks.")
            
            if st.button("⚖️ Run Agentic Analysis"):
                with st.spinner("Local LLM Reasoning..."):
                    verdict = run_local_judge(ticker, query, "OpenAI" if engine == "OpenAI (Key Required)" else "Local", api_key)
                    st.markdown("### Agent Verdict")
                    st.markdown(verdict)
