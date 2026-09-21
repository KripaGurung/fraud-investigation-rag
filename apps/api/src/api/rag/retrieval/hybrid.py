from dataclasses import dataclass

from sqlalchemy.orm import Session

from api.rag.retrieval.keyword import keyword_search
from api.rag.retrieval.semantic import semantic_search


@dataclass(frozen=True)
class HybridSearchResult:
    chunk_id: int
    document_reference: str
    document_type: str
    title: str
    source: str
    chunk_index: int
    content: str
    semantic_score: float
    keyword_score: float
    score: float


def hybrid_search(
    db: Session,
    query: str,
    limit: int = 5,
    document_type: str | None = None,
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> list[HybridSearchResult]:
    if not query.strip():
        raise ValueError("query must not be empty")

    if limit < 1:
        raise ValueError("limit must be at least 1")

    if semantic_weight < 0 or keyword_weight < 0:
        raise ValueError("weights must not be negative")

    total_weight = semantic_weight + keyword_weight

    if total_weight <= 0:
        raise ValueError("at least one retrieval weight must be greater than 0")

    semantic_weight /= total_weight
    keyword_weight /= total_weight

    retrieval_limit = max(limit * 2, 10)

    semantic_results = semantic_search(
        db=db,
        query=query,
        limit=retrieval_limit,
        document_type=document_type,
    )

    keyword_results = keyword_search(
        db=db,
        query=query,
        limit=retrieval_limit,
        document_type=document_type,
    )

    combined: dict[int, dict[str, object]] = {}

    for result in semantic_results:
        combined[result.chunk_id] = {
            "chunk_id": result.chunk_id,
            "document_reference": result.document_reference,
            "document_type": result.document_type,
            "title": result.title,
            "source": result.source,
            "chunk_index": result.chunk_index,
            "content": result.content,
            "semantic_score": result.score,
            "keyword_score": 0.0,
        }

    for result in keyword_results:
        if result.chunk_id not in combined:
            combined[result.chunk_id] = {
                "chunk_id": result.chunk_id,
                "document_reference": result.document_reference,
                "document_type": result.document_type,
                "title": result.title,
                "source": result.source,
                "chunk_index": result.chunk_index,
                "content": result.content,
                "semantic_score": 0.0,
                "keyword_score": result.score,
            }
        else:
            combined[result.chunk_id]["keyword_score"] = result.score

    results: list[HybridSearchResult] = []

    for item in combined.values():
        semantic_score = float(item["semantic_score"])
        keyword_score = float(item["keyword_score"])

        score = (
            semantic_weight * semantic_score
            + keyword_weight * keyword_score
        )

        results.append(
            HybridSearchResult(
                chunk_id=int(item["chunk_id"]),
                document_reference=str(item["document_reference"]),
                document_type=str(item["document_type"]),
                title=str(item["title"]),
                source=str(item["source"]),
                chunk_index=int(item["chunk_index"]),
                content=str(item["content"]),
                semantic_score=semantic_score,
                keyword_score=keyword_score,
                score=score,
            )
        )

    results.sort(
        key=lambda result: (
            -result.score,
            -result.semantic_score,
            -result.keyword_score,
            result.chunk_id,
        )
    )

    return results[:limit]