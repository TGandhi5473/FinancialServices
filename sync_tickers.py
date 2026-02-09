import requests
import pandas as pd
import os

def sync_sec_tickers():
    url = "https://www.sec.gov/files/company_tickers.json"
    # Note: SEC requires a descriptive User-Agent
    headers = {"User-Agent": "TickerSyncBot contact@example.com"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Convert SEC JSON format to clean CSV
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.rename(columns={'ticker': 'Symbol', 'title': 'Name'})
        
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/us_tickers.csv", index=False)
        print(f"✅ Successfully synced {len(df)} tickers to data/us_tickers.csv")
    except Exception as e:
        print(f"❌ Failed to sync tickers: {e}")

if __name__ == "__main__":
    sync_sec_tickers()
