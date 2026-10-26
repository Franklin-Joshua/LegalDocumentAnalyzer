import streamlit as st
from input_module import read_document
from preprocessing_module import preprocess_document, split_chunks
from analyzer_module import analyze_document
from save_module import save_analysis, format_analysis
from utils import check_ollama

st.set_page_config(page_title="Legal Document Analyzer", page_icon="⚖️", layout="wide")
st.title("Automated Legal Document Analyzer")
st.caption("Powered by local Ollama · Qwen3:4b")
st.warning("Informational summary only, not legal advice. Have a qualified legal professional review important decisions.")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Ollama model", "qwen3:4b")
    chunk_size = st.slider("Chunk size (characters)", 1500, 6000, 3500, 500)
    if st.button("Check Ollama connection"):
        ok, msg = check_ollama(model)
        st.success(msg) if ok else st.error(msg)

st.header("1. Upload or enter legal document")
document, filename = read_document()
if document:
    cleaned = preprocess_document(document)
    st.caption(f"Source: {filename} · Original: {len(document):,} chars · Cleaned: {len(cleaned):,} chars")
    with st.expander("Preview extracted text"):
        st.text(cleaned[:12000] + ("\n[Preview truncated]" if len(cleaned) > 12000 else ""))
    if st.button("Analyze document", type="primary", use_container_width=True):
        try:
            chunks = split_chunks(cleaned, chunk_size)
            st.info(f"Prepared {len(chunks)} section(s).")
            progress = st.progress(0)
            notes = []
            for i, chunk in enumerate(chunks):
                with st.spinner(f"Analyzing section {i+1}/{len(chunks)} using {model}..."):
                    notes.append(analyze_document(chunk, model, partial=len(chunks) > 1))
                progress.progress((i+1)/len(chunks))
            analysis = notes[0] if len(notes) == 1 else analyze_document("\n\n".join(notes), model)
            st.session_state["legal_analysis"] = analysis
            st.session_state["legal_source_name"] = filename
            st.success("Analysis completed.")
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.info("Check Ollama is running, the model is installed, and the document is not too large.")

if "legal_analysis" in st.session_state:
    st.divider()
    st.header("2. Legal document analysis")
    st.markdown(st.session_state["legal_analysis"])
    st.caption("Verify findings against the original document. This is not legal advice.")
    if st.button("Save analysis to outputs/legal_analysis.txt", use_container_width=True):
        try:
            path = save_analysis(st.session_state["legal_source_name"], st.session_state["legal_analysis"])
            st.success(f"Saved to {path}")
        except Exception as e:
            st.error(f"Could not save: {e}")
    st.download_button("Download analysis report",
        format_analysis(st.session_state["legal_source_name"], st.session_state["legal_analysis"]),
        file_name="legal_analysis.txt", mime="text/plain")
