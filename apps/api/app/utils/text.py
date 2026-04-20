from __future__ import annotations

import re


def normalize_query(query: str) -> str:
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def rough_token_count(text: str) -> int:
    return max(1, len(text.split()))


def sentence_windows(text: str, max_words: int = 140) -> list[str]:
    paragraphs = [segment.strip() for segment in re.split(r"\n\s*\n", text) if segment.strip()]
    windows: list[str] = []
    buffer: list[str] = []
    size = 0
    for paragraph in paragraphs:
        paragraph_words = paragraph.split()
        if size + len(paragraph_words) > max_words and buffer:
            windows.append("\n\n".join(buffer))
            buffer = [paragraph]
            size = len(paragraph_words)
        else:
            buffer.append(paragraph)
            size += len(paragraph_words)
    if buffer:
        windows.append("\n\n".join(buffer))
    return windows or [text]

