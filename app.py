import streamlit as st
import pandas as pd
import os
from src.scraper import collect_financials
from src.ingester import create_vector_store
from src.judge import run_local_judge
from src.evaluator import get_audit_summary

# 1. Page Configuration
st.set_page_config(page_title="Fin-Agent Judge", layout="wide", page_icon="⚖️")

# 2. Sidebar: Identity, Engine, and Settings
with st.sidebar:
    st.header("🔑 Credentials")
    user_email = st.text_input("SEC User-Agent Email", placeholder="analyst@firm.com")
    st.divider()
    
    st.header("⚙️ Agent Settings")
    engine = st.radio("Reasoning Engine", ["Local (DeepSeek-R1)", "Cloud (GPT-4o)"])
    api_key = st.text_input("OpenAI Key", type="password") if "Cloud" in engine else None
    
    high_precision = st.toggle(
        "High Precision Mode", 
        value=True, 
        help="Enables a secondary 'Senior Auditor' agent to verify the Analyst's findings."
    )

    # 3. Occasional Log Analysis (Audit Viewer)
    st.divider()
    with st.expander("📊 Audit History & Evals"):
        if st.button("Refresh History"):
            history_df = get_audit_summary()
            if history_df is not None:
                # Display high-level metrics
                refinement_rate = (history_df['was_refined'].sum() / len(history_df)) * 100
                st.metric("Refinement Rate", f"{refinement_rate:.1f}%")
                
                # Show comparison table
                st.dataframe(
                    history_df[['timestamp', 'ticker', 'was_refined']],
                    use_container_width=True,
                    hide_index=True
                )
                
                if st.checkbox("Show Detailed Drafts"):
                    st.json(history_df[['analyst_draft', 'final_verdict']].to_dict('records'))
            else:
                st.info("No audit logs found.")

# 4. Main Interface
st.title("🛡️ Fin-Agent Judge")
st.caption("Local SEC Ingestion & Dual-Agent Financial Auditing")

TICKER_PATH = "data/us_tickers.csv"

if os.path.exists(TICKER_PATH):
    # Load and format ticker list
    ticker_df = pd.read_csv(TICKER_PATH)
    ticker_options = (ticker_df['Symbol'] + " - " + ticker_df['Name']).tolist()
    selection = st.selectbox("Select Target Company", options=ticker_options, index=None)
    
    if selection:
        ticker = selection.split(" - ")[0]
        
        if not user_email:
            st.warning("⚠️ Identity Required: Enter your email in the sidebar to comply with SEC policies.")
        else:
            db_path = f"vector_db/{ticker}"
            
            # Check for local knowledge base
            if not os.path.exists(db_path):
                st.info(f"Knowledge base for {ticker} not found. Ingestion required.")
                if st.button(f"Scrape & Index {ticker}"):
                    with st.status(f"Processing {ticker}...", expanded=True) as status:
                        st.write("Downloading 10-K sections...")
                        json_path = collect_financials(ticker, user_email)
                        st.write("Generating local embeddings...")
                        create_vector_store(json_path, ticker)
                        status.update(label="Ready for Analysis!", state="complete")
                    st.rerun()
            else:
                # --- Analysis Phase ---
                st.success(f"✅ {ticker} Context Loaded.")
                query = st.text_area("Audit Query:", "What are the primary liquidity risks mentioned?")
                
                if st.button("⚖️ Run Agentic Audit"):
                    with st.status("Agentic Process Initialized...") as status:
                        st.write("Step 1: Analyst pass (Synthesizing data)...")
                        
                        # Execute Dual-Agent Logic
                        verdict = run_local_judge(
                            ticker=ticker, 
                            query=query, 
                            mode="OpenAI" if "Cloud" in engine else "Local", 
                            api_key=api_key,
                            high_precision=high_precision
                        )
                        
                        status.update(label="Audit Complete!", state="complete")
                    
                    st.subheader("Final Agent Verdict")
                    st.markdown(verdict)
                    
                    if high_precision:
                        st.info("💡 Note: This verdict was verified by the Senior Auditor pass.")
else:
    st.error("Missing `data/us_tickers.csv`. Please run `python sync_tickers.py` to initialize.")


