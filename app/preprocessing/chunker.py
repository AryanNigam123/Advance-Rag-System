import uuid
from typing import List, Dict
from app.config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(page: Dict) -> List[Dict]:
    """
    Splits cleaned page text into overlapping chunks.
    Preserves metadata for each chunk.
    """

    text = page["text"]
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE
        chunk_text = text[start:end]

        if chunk_text.strip():
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "session_id": page["session_id"],
                "source_pdf": page["source_pdf"],
                "page_number": page["page_number"],
                "chunk_text": chunk_text
            })

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
