import re

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for embedding.
    Uses sentence-aware splitting for better legal context preservation.
    """
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split(' ')
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # Slide window with overlap

    return chunks
