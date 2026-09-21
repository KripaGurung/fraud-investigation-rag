import pytest

from api.rag.ingestion.embeddings import (
    EMBEDDING_DIMENSION,
    generate_embedding,
)


def test_generate_embedding_returns_expected_dimension() -> None:
    embedding = generate_embedding(
        "unusual high-value international transfer"
    )

    assert isinstance(embedding, list)
    assert len(embedding) == EMBEDDING_DIMENSION
    assert all(isinstance(value, float) for value in embedding)


def test_generate_embedding_rejects_empty_text() -> None:
    with pytest.raises(
        ValueError,
        match="text must not be empty",
    ):
        generate_embedding("   ")