from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import KnowledgeChunk, KnowledgeDocument
from api.rag.corpus.schema import CorpusDocument
from api.rag.ingestion.embeddings import EMBEDDING_DIMENSION
from api.rag.ingestion.pipeline import ingest_document


def test_ingest_document_creates_document_and_chunks(
    db: Session,
) -> None:
    document = CorpusDocument(
        document_reference="TEST-INGEST-001",
        document_type="historical_fraud_case",
        title="Test Ingestion Document",
        source="test_suite",
        content=(
            "one two three four five six seven eight nine ten"
        ),
    )

    ingest_document(
        db,
        document,
    )

    db.flush()

    stored_document = db.scalar(
        select(KnowledgeDocument).where(
            KnowledgeDocument.document_reference
            == document.document_reference
        )
    )

    assert stored_document is not None
    assert stored_document.document_type == document.document_type
    assert stored_document.title == document.title
    assert stored_document.source == document.source
    assert stored_document.content == document.content

    stored_chunks = list(
        db.scalars(
            select(KnowledgeChunk)
            .where(
                KnowledgeChunk.document_id == stored_document.id
            )
            .order_by(KnowledgeChunk.chunk_index)
        ).all()
    )

    assert len(stored_chunks) == 1

    stored_chunk = stored_chunks[0]

    assert stored_chunk.chunk_index == 0
    assert stored_chunk.content == document.content

    assert stored_chunk.embedding is not None
    assert len(stored_chunk.embedding) == EMBEDDING_DIMENSION

    db.rollback()