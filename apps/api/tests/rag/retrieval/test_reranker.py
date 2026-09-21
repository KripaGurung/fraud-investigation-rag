from api.rag.retrieval.hybrid import HybridSearchResult
from api.rag.retrieval.reranker import rerank_results


class FakeRerankerModel:
    def predict(
        self,
        pairs: list[list[str]],
    ) -> list[float]:
        scores = []

        for _, content in pairs:
            if "strong match" in content:
                scores.append(3.0)
            elif "medium match" in content:
                scores.append(1.0)
            else:
                scores.append(-1.0)

        return scores


def make_result(
    chunk_id: int,
    content: str,
    score: float,
) -> HybridSearchResult:
    return HybridSearchResult(
        chunk_id=chunk_id,
        document_reference=f"DOC-{chunk_id}",
        document_type="historical_fraud_case",
        title=f"Document {chunk_id}",
        source="test-source",
        chunk_index=0,
        content=content,
        semantic_score=score,
        keyword_score=score,
        score=score,
    )


def test_rerank_results_orders_by_reranker_score() -> None:
    results = [
        make_result(
            chunk_id=1,
            content="weak match",
            score=0.95,
        ),
        make_result(
            chunk_id=2,
            content="strong match",
            score=0.60,
        ),
        make_result(
            chunk_id=3,
            content="medium match",
            score=0.80,
        ),
    ]

    reranked = rerank_results(
        query="fraud investigation",
        results=results,
        limit=3,
        model=FakeRerankerModel(),
    )

    assert [result.chunk_id for result in reranked] == [2, 3, 1]


def test_rerank_results_preserves_hybrid_scores() -> None:
    results = [
        make_result(
            chunk_id=1,
            content="strong match",
            score=0.75,
        ),
    ]

    reranked = rerank_results(
        query="fraud investigation",
        results=results,
        limit=1,
        model=FakeRerankerModel(),
    )

    result = reranked[0]

    assert result.semantic_score == 0.75
    assert result.keyword_score == 0.75
    assert result.hybrid_score == 0.75
    assert 0.0 <= result.rerank_score <= 1.0
    assert result.score == result.rerank_score


def test_rerank_results_respects_limit() -> None:
    results = [
        make_result(1, "weak match", 0.9),
        make_result(2, "strong match", 0.8),
        make_result(3, "medium match", 0.7),
    ]

    reranked = rerank_results(
        query="fraud investigation",
        results=results,
        limit=2,
        model=FakeRerankerModel(),
    )

    assert len(reranked) == 2
    assert [result.chunk_id for result in reranked] == [2, 3]


def test_rerank_results_handles_empty_results() -> None:
    reranked = rerank_results(
        query="fraud investigation",
        results=[],
        limit=5,
        model=FakeRerankerModel(),
    )

    assert reranked == []


def test_rerank_results_rejects_empty_query() -> None:
    try:
        rerank_results(
            query="   ",
            results=[],
            limit=5,
            model=FakeRerankerModel(),
        )
    except ValueError as exc:
        assert str(exc) == "query must not be empty"
    else:
        raise AssertionError("Expected ValueError")


def test_rerank_results_rejects_invalid_limit() -> None:
    try:
        rerank_results(
            query="fraud investigation",
            results=[],
            limit=0,
            model=FakeRerankerModel(),
        )
    except ValueError as exc:
        assert str(exc) == "limit must be at least 1"
    else:
        raise AssertionError("Expected ValueError")