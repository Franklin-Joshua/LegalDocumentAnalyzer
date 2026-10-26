import streamlit as st
from io import BytesIO

def _extract_pdf(data):
    try:
        from pypdf import PdfReader
    except ImportError:
        raise RuntimeError("PDF support missing. Run: pip install pypdf")
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_document():
    mode = st.radio("Input method", ["Paste text", "Upload file"], horizontal=True)
    if mode == "Paste text":
        text = st.text_area("Legal document text", height=260,
                            placeholder="Paste the contract or legal document here...")
        return (text.strip(), "Pasted document") if text.strip() else ("", "")
    uploaded = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    if not uploaded:
        return "", ""
    data = uploaded.getvalue()
    try:
        text = _extract_pdf(data) if uploaded.name.lower().endswith(".pdf") else data.decode("utf-8", errors="replace")
    except Exception as e:
        st.error(str(e))
        return "", ""
    if not text.strip():
        st.error("No readable text found. Scanned PDFs may need OCR first.")
        return "", ""
    return text, uploaded.name
