def chunk_text(text, max_chars=1200):
    chunks = []
    current = ""

    for line in text.splitlines():
        if len(current) + len(line) < max_chars:
            current += line + "\n"
        else:
            chunks.append(current)
            current = line + "\n"

    if current.strip():
        chunks.append(current)

    return chunks