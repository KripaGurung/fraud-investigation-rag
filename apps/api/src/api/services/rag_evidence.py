from api.schemas.evidence import EvidenceItem
from api.rag.retrieval.hybrid import HybridSearchResult


def retrieval_result_to_evidence(
    result: HybridSearchResult,
) -> EvidenceItem:
    return EvidenceItem(
        source_id=result.document_reference,
        source_type=result.document_type,
        content=result.content,
        score=result.score,
        metadata={
            "title": result.title,
            "source": result.source,
            "chunk_id": result.chunk_id,
            "chunk_index": result.chunk_index,
            "semantic_score": result.semantic_score,
            "keyword_score": result.keyword_score,
        },
    )