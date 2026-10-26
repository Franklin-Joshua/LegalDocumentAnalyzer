import re

def preprocess_document(text):
    text = text.replace("\x00", " ").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", text)
    return text.strip()

def split_chunks(text, max_chars=3500):
    if len(text) <= max_chars:
        return [text]
    chunks, current = [], ""
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(paragraph[i:i+max_chars] for i in range(0, len(paragraph), max_chars))
        elif len(current) + len(paragraph) + 1 <= max_chars:
            current = (current + "\n" + paragraph).strip()
        else:
            if current:
                chunks.append(current)
            current = paragraph
    if current:
        chunks.append(current)
    return chunks or [text[:max_chars]]
