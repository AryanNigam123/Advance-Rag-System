from typing import List, Dict

def extract_text_by_page(doc) -> List[Dict]:
    """
    Extracts text from each page of a PDF document.
    Returns a list of dictionaries with page number and text.
    """
    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page_number": page_index + 1,
                "text": text
            })

    return pages
