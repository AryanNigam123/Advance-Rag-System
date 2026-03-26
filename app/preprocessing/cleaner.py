import re

def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text by:
    - Removing extra whitespace
    - Normalizing newlines
    - Removing non-printable characters
    """

    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n{2,}", "\n", text)

    # Replace multiple spaces with single space
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()
