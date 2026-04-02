def chunk_text(page_text: str) -> list[str]:
    chunks: list[str] = []
    for part in page_text.split("\n\n"):
        cleaned = " ".join(part.split())
        if cleaned:
            chunks.append(cleaned)
    return chunks
