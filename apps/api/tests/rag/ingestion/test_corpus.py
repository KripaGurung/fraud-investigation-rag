from unittest.mock import Mock

from api.rag.ingestion.corpus import (
    CORPUS_DOCUMENTS,
    ingest_corpus,
)


def test_corpus_contains_expected_documents() -> None:
    document_references = {
        document.document_reference
        for document in CORPUS_DOCUMENTS
    }

    assert len(CORPUS_DOCUMENTS) == 5

    assert document_references == {
        "CASE-001",
        "CASE-002",
        "CASE-003",
        "POLICY-AML-001",
        "POLICY-AML-002",
    }


def test_ingest_corpus_ingests_every_document(
    monkeypatch,
) -> None:
    mock_ingest_document = Mock()

    monkeypatch.setattr(
        "api.rag.ingestion.corpus.ingest_document",
        mock_ingest_document,
    )

    mock_db = Mock()

    ingest_corpus(mock_db)

    assert mock_ingest_document.call_count == len(
        CORPUS_DOCUMENTS
    )

    for document in CORPUS_DOCUMENTS:
        mock_ingest_document.assert_any_call(
            db=mock_db,
            document=document,
        )