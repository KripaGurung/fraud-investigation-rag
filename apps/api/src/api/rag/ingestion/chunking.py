from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    content: str


def chunk_text(
    text: str,
    chunk_size: int = 120,
    chunk_overlap: int = 20,
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    words = text.split()

    if not words:
        return []

    step = chunk_size - chunk_overlap
    chunks: list[TextChunk] = []

    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size]

        chunks.append(
            TextChunk(
                chunk_index=len(chunks),
                content=" ".join(chunk_words),
            )
        )

        if start + chunk_size >= len(words):
            break

    return chunks
