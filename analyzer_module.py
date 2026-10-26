from utils import ask_ollama
from prompt_module import build_prompt

def analyze_document(document, model="qwen3:4b", partial=False):
    return ask_ollama(build_prompt(document, partial), model, temperature=0.1, max_tokens=700)
