# Automated Legal Document Analyzer — Qwen3:4b

Streamlit app using local Ollama to summarize legal text and extract structured contract details.

## Features
- Paste legal text or upload `.txt` / text-based `.pdf`
- Text normalization and chunking for long documents
- Summary, parties, purpose, obligations, payment, duration, termination, dates and key clauses
- Save report to `outputs/legal_analysis.txt` or download it

## Windows setup
```powershell
ollama pull qwen3:4b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run main.py
```

Ollama should run at `http://localhost:11434`. Scanned PDFs may require OCR. Review all findings against the original document; this tool does not provide legal advice.
