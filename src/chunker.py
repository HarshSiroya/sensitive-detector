from typing import List, Dict
import re

def _find_split_points(text: str, start: int, max_chars: int) -> int:
    """
    find best split points
    """
    window = text[start: start + max_chars]

    last_newline = window.rfind("\n")
    last_period = window.rfind(".")
    last_comma = window.rfind(";")
    last_exclamation = window.rfind("!")
    last_question = window.rfind("?")
    
    # Fix spelling + include all candidates
    candidates = [last_newline, last_period, last_comma, last_exclamation, last_question]
    best = max(candidates)

    if best <= 0:
        return start + len(window)

    return start + best + 1


def chunk_text(text: str, max_chars: int = 1500, overlap: int = 200) -> List[Dict]:
    """
    Split text into overlapping chunks.
    Returns a list of dicts
    """
    if max_chars <= overlap:
        raise ValueError("max_chars must be greater than overlap")
    
    text_len = len(text)
    chunks: List[Dict] = []
    start = 0
    chunk_id = 0

    step = max_chars - overlap

    while start < text_len:
        end = _find_split_points(text, start, max_chars)

        if end <= start:
            end = min(start + max_chars, text_len)

        chunk_text_value = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text_value,
            "start_char": start,
            "end_char": end
        })

        start += step
        chunk_id += 1

    return chunks
