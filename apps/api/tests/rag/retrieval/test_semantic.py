import pytest
from sqlalchemy.orm import Session

from api.rag.retrieval.semantic import semantic_search


def test_semantic_search_returns_relevant_historical_case(
    db: Session,
) -> None:
    results = semantic_search(
        db=db,
        query=(
            "large international transfer from an unfamiliar "
            "device to a new beneficiary"
        ),
        limit=3,
        document_type="historical_fraud_case",
    )

    assert results
    assert len(results) <= 3

    assert results[0].document_reference == "CASE-001"
    assert results[0].document_type == "historical_fraud_case"
    assert results[0].score >= 0.0
    assert results[0].score <= 1.0


def test_semantic_search_filters_by_document_type(
    db: Session,
) -> None:
    results = semantic_search(
        db=db,
        query="unusual transaction activity requiring review",
        limit=5,
        document_type="aml_policy",
    )

    assert results

    assert all(
        result.document_type == "aml_policy"
        for result in results
    )


def test_semantic_search_rejects_empty_query(
    db: Session,
) -> None:
    with pytest.raises(
        ValueError,
        match="query must not be empty",
    ):
        semantic_search(
            db=db,
            query="   ",
        )


def test_semantic_search_rejects_invalid_limit(
    db: Session,
) -> None:
    with pytest.raises(
        ValueError,
        match="limit must be at least 1",
    ):
        semantic_search(
            db=db,
            query="international transfer",
            limit=0,
        )