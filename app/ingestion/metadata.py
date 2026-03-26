from typing import List, Dict

def attach_metadata(
    pages: List[Dict],
    session_id: str,
    source_pdf: str
) -> List[Dict]:
    """
    Attaches metadata to extracted page text.
    """
    enriched_pages = []

    for page in pages:
        enriched_pages.append({
            "session_id": session_id,
            "source_pdf": source_pdf,
            "page_number": page["page_number"],
            "text": page["text"]
        })

    return enriched_pages
