import requests
import pandas as pd
import os

def sync():
    """Fetches the official CIK-Ticker mapping from SEC.gov."""
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": "ResearchProject analyst@example.com"} # Change to your email
    
    print("🔄 Syncing US Tickers from SEC...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.rename(columns={'ticker': 'Symbol', 'title': 'Name', 'cik_str': 'CIK'})
        
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/us_tickers.csv", index=False)
        print(f"✅ Successfully saved {len(df)} tickers to data/us_tickers.csv")
    else:
        print(f"❌ Failed to sync: {response.status_code}")

if __name__ == "__main__":
    sync()
    
