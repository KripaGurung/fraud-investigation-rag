from dataclasses import dataclass

from sqlalchemy import Integer, String, cast, func
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.models import KnowledgeChunk, KnowledgeDocument


@dataclass(frozen=True)
class KeywordSearchResult:
    chunk_id: int
    document_reference: str
    document_type: str
    title: str
    source: str
    chunk_index: int
    content: str
    score: float


def keyword_search(
    db: Session,
    query: str,
    limit: int = 5,
    document_type: str | None = None,
) -> list[KeywordSearchResult]:
    if not query.strip():
        raise ValueError("query must not be empty")

    if limit < 1:
        raise ValueError("limit must be at least 1")

    search_terms = [
        term.lower()
        for term in query.split()
        if term.strip()
    ]

    if not search_terms:
        raise ValueError("query must contain searchable terms")

    searchable_text = func.lower(
        cast(
            KnowledgeChunk.content,
            String,
        )
    )

    term_matches = [
        cast(
            searchable_text.contains(term),
            Integer,
        )
        for term in search_terms
    ]

    match_score = sum(
        term_matches,
        start=0,
    )

    statement = (
        select(
            KnowledgeChunk,
            KnowledgeDocument,
            match_score.label("match_score"),
        )
        .join(
            KnowledgeDocument,
            KnowledgeChunk.document_id == KnowledgeDocument.id,
        )
        .where(
            KnowledgeChunk.content.is_not(None),
            match_score > 0,
        )
    )

    if document_type is not None:
        statement = statement.where(
            KnowledgeDocument.document_type == document_type
        )

    statement = (
        statement
        .order_by(
            match_score.desc(),
            KnowledgeChunk.id,
        )
        .limit(limit)
    )

    rows = db.execute(statement).all()

    results: list[KeywordSearchResult] = []

    total_terms = len(search_terms)

    for chunk, document, raw_score in rows:
        score = float(raw_score) / total_terms

        results.append(
            KeywordSearchResult(
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