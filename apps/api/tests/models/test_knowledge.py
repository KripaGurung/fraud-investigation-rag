from sqlalchemy.orm import Session

from api.models import KnowledgeChunk, KnowledgeDocument


def test_knowledge_document_chunk_relationship(
    db: Session,
) -> None:
    document = KnowledgeDocument(
        document_reference="TEST-CASE-001",
        document_type="historical_fraud_case",
        title="Test Historical Fraud Case",
        source="test_suite",
        content=(
            "A customer made an unusually large international "
            "transfer to a new beneficiary."
        ),
    )

    chunk_1 = KnowledgeChunk(
        document=document,
        chunk_index=0,
        content="The customer made an unusually large transfer.",
    )

    chunk_2 = KnowledgeChunk(
        document=document,
        chunk_index=1,
        content="The transfer was sent to a new international beneficiary.",
    )

    db.add(document)
    db.flush()

    assert document.id is not None
    assert chunk_1.id is not None
    assert chunk_2.id is not None

    assert document.chunks == [
        chunk_1,
        chunk_2,
    ]

    assert chunk_1.document is document
    assert chunk_2.document is document

    assert chunk_1.document_id == document.id
    assert chunk_2.document_id == document.id

    db.rollback()