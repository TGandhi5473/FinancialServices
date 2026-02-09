import os
import json
from edgar import Company, set_identity

def collect_financials(ticker, user_email):
    """Deterministic extraction of 10-K sections and XBRL facts."""
    set_identity(user_email)
    company = Company(ticker)
    
    output_dir = f"data/filings/{ticker}"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Fetch Latest 10-K
    tenk_filing = company.get_filings(form="10-K").latest()
    tenk = tenk_filing.obj()
    
    # 2. Extract Narrative Sections
    # These properties are parsed by edgartools into readable text/markdown
    narrative = {
        "risk_factors": getattr(tenk, 'risk_factors', "Section 1A (Risk Factors) not found."),
        "md_and_a": getattr(tenk, 'management_discussion', "Section 7 (MD&A) not found."),
        "legal_proceedings": getattr(tenk, 'legal_proceedings', "Section 3 not found.")
    }
    
    json_path = os.path.join(output_dir, "narrative.json")
    with open(json_path, "w") as f:
        json.dump(narrative, f)
        
    # 3. Save raw facts for potential math verification (Optional)
    facts = company.get_facts().to_pandas()
    facts.to_csv(os.path.join(output_dir, "facts.csv"), index=False)
        
    return json_path
