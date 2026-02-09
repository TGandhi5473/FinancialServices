import pandas as pd
import json
import os

def get_audit_summary():
    """
    Parses the local audit_trail.jsonl file into a DataFrame 
    for session analysis and progress tracking.
    """
    log_path = "logs/audit_trail.jsonl"
    
    if not os.path.exists(log_path):
        return None
    
    data = []
    try:
        with open(log_path, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        
        if not data:
            return None
            
        df = pd.DataFrame(data)
        # Clean up timestamp for display
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        return df
    except Exception as e:
        print(f"Error reading logs: {e}")
        return None
