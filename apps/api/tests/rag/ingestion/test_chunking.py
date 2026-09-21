import pytest

from api.rag.ingestion.chunking import TextChunk, chunk_text


def test_chunk_text_with_overlap() -> None:
    text = "one two three four five six seven eight nine ten"

    chunks = chunk_text(
        text,
        chunk_size=4,
        chunk_overlap=1,
    )

    assert chunks == [
        TextChunk(
            chunk_index=0,
            content="one two three four",
        ),
        TextChunk(
            chunk_index=1,
            content="four five six seven",
        ),
        TextChunk(
            chunk_index=2,
            content="seven eight nine ten",
        ),
    ]


def test_chunk_text_returns_empty_list_for_empty_text() -> None:
    assert chunk_text("") == []
    assert chunk_text("   \n\t   ") == []


def test_chunk_text_rejects_non_positive_chunk_size() -> None:
    with pytest.raises(
        ValueError,
        match="chunk_size must be greater than zero",
    ):
        chunk_text(
            "one two three",
            chunk_size=0,
        )


def test_chunk_text_rejects_negative_overlap() -> None:
    with pytest.raises(
        ValueError,
        match="chunk_overlap cannot be negative",
    ):
        chunk_text(
            "one two three",
            chunk_overlap=-1,
        )


def test_chunk_text_rejects_overlap_equal_to_chunk_size() -> None:
    with pytest.raises(
        ValueError,
        match="chunk_overlap must be smaller than chunk_size",
    ):
        chunk_text(
            "one two three four",
            chunk_size=4,
            chunk_overlap=4,
        )
