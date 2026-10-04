from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import KnowledgeChunk, KnowledgeDocument
from api.rag.ingestion.embeddings import generate_embedding


@dataclass(frozen=True)
class SemanticSearchResult:
    chunk_id: int
    document_reference: str
    document_type: str
    title: str
    source: str
    chunk_index: int
    content: str
    score: float


def semantic_search(
    db: Session,
    query: str,
    limit: int = 5,
    document_type: str | None = None,
) -> list[SemanticSearchResult]:
    if not query.strip():
        raise ValueError("query must not be empty")

    if limit < 1:
        raise ValueError("limit must be at least 1")

    query_embedding = generate_embedding(query)

    cosine_distance = KnowledgeChunk.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            KnowledgeChunk,
            KnowledgeDocument,
            cosine_distance.label("distance"),
        )
        .join(
            KnowledgeDocument,
            KnowledgeChunk.document_id == KnowledgeDocument.id,
        )
        .where(KnowledgeChunk.embedding.is_not(None))
    )

    if document_type is not None:
        statement = statement.where(
            KnowledgeDocument.document_type == document_type
        )

    statement = statement.order_by(cosine_distance).limit(limit)

    rows = db.execute(statement).all()

    results: list[SemanticSearchResult] = []

    for chunk, document, distance in rows:
        score = max(
            0.0,
            min(1.0, 1.0 - (float(distance) / 2.0)),
        )

        results.append(
            SemanticSearchResult(
                chunk_id=chunk.id,
                document_reference=document.document_reference,
                document_type=document.document_type,
                title=document.title,
                source=document.source,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                score=score,
            )
        )

    return results