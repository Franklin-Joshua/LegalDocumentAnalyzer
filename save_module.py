import os
from datetime import datetime

def format_analysis(source_name, analysis):
    return ("AUTOMATED LEGAL DOCUMENT ANALYSIS\n" + "="*40 + "\n"
            + f"Source: {source_name}\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
            + analysis.strip() + "\n\nDISCLAIMER: AI-generated informational summary, not legal advice.\n")

def save_analysis(source_name, analysis):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "legal_analysis.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(format_analysis(source_name, analysis) + "\n" + "-"*70 + "\n")
    return path
