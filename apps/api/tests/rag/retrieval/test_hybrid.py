from sqlalchemy.orm import Session

from api.rag.retrieval.hybrid import hybrid_search


def test_hybrid_search_returns_relevant_historical_case(
    db: Session,
) -> None:
    results = hybrid_search(
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

    assert results[0].semantic_score > 0.0
    assert results[0].keyword_score > 0.0
    assert results[0].score > 0.0


def test_hybrid_search_filters_by_document_type(
    db: Session,
) -> None:
    results = hybrid_search(
        db=db,
        query="unusual transaction velocity requiring review",
        limit=5,
        document_type="aml_policy",
    )

    assert results

    assert all(
        result.document_type == "aml_policy"
        for result in results
    )


def test_hybrid_search_scores_are_normalized(
    db: Session,
) -> None:
    results = hybrid_search(
        db=db,
        query="international transfer unfamiliar device",
        limit=5,
    )

    assert results

    for result in results:
        assert 0.0 <= result.semantic_score <= 1.0
        assert 0.0 <= result.keyword_score <= 1.0
        assert 0.0 <= result.score <= 1.0


def test_hybrid_search_rejects_empty_query(
    db: Session,
) -> None:
    import pytest

    with pytest.raises(
        ValueError,
        match="query must not be empty",
    ):
        hybrid_search(
            db=db,
            query="   ",
        )


def test_hybrid_search_rejects_invalid_limit(
    db: Session,
) -> None:
    import pytest

    with pytest.raises(
        ValueError,
        match="limit must be at least 1",
    ):
        hybrid_search(
            db=db,
            query="international transfer",
            limit=0,
        )


def test_hybrid_search_rejects_negative_weights(
    db: Session,
) -> None:
    import pytest

    with pytest.raises(
        ValueError,
        match="weights must not be negative",
    ):
        hybrid_search(
            db=db,
            query="international transfer",
            semantic_weight=-0.1,
        )


def test_hybrid_search_rejects_zero_total_weight(
    db: Session,
) -> None:
    import pytest

    with pytest.raises(
        ValueError,
        match="at least one retrieval weight must be greater than 0",
    ):
        hybrid_search(
            db=db,
            query="international transfer",
            semantic_weight=0.0,
            keyword_weight=0.0,
        )