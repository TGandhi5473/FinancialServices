import pandas as pd
import json
import os

def get_audit_summary():
    log_path = "logs/audit_trail.jsonl"
    if not os.path.exists(log_path):
        return None
    
    data = []
    with open(log_path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    
    df = pd.DataFrame(data)
    # Convert ISO timestamp to readable format
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    return df



