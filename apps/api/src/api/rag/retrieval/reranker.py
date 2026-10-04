from dataclasses import dataclass
from functools import lru_cache
from math import exp
from typing import Protocol

from sentence_transformers import CrossEncoder

from api.rag.retrieval.hybrid import HybridSearchResult


RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class RerankerModel(Protocol):
    def predict(
        self,
        pairs: list[list[str]],
    ) -> object:
        ...


@dataclass(frozen=True)
class RerankedSearchResult:
    chunk_id: int
    document_reference: str
    document_type: str
    title: str
    source: str
    chunk_index: int
    content: str
    semantic_score: float
    keyword_score: float
    hybrid_score: float
    rerank_score: float
    score: float


@lru_cache(maxsize=1)
def get_reranker_model() -> CrossEncoder:
    return CrossEncoder(RERANKER_MODEL_NAME)


def _sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + exp(-value))

    exponential = exp(value)
    return exponential / (1.0 + exponential)


def rerank_results(
    query: str,
    results: list[HybridSearchResult],
    limit: int = 5,
    model: RerankerModel | None = None,
) -> list[RerankedSearchResult]:
    if not query.strip():
        raise ValueError("query must not be empty")

    if limit < 1:
        raise ValueError("limit must be at least 1")

    if not results:
        return []

    reranker = model or get_reranker_model()

    pairs = [
        [query, result.content]
        for result in results
    ]

    raw_scores = reranker.predict(pairs)

    reranked_results: list[RerankedSearchResult] = []

    for result, raw_score in zip(
        results,
        raw_scores,
        strict=True,
    ):
        rerank_score = _sigmoid(float(raw_score))

        reranked_results.append(
            RerankedSearchResult(
                chunk_id=result.chunk_id,
                document_reference=result.document_reference,
                document_type=result.document_type,
                title=result.title,
                source=result.source,
                chunk_index=result.chunk_index,
                content=result.content,
                semantic_score=result.semantic_score,
                keyword_score=result.keyword_score,
                hybrid_score=result.score,
                rerank_score=rerank_score,
                score=rerank_score,
            )
        )

    reranked_results.sort(
        key=lambda result: (
            -result.rerank_score,
            -result.hybrid_score,
            result.chunk_id,
        )
    )

    return reranked_results[:limit]