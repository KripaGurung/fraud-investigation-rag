from api.rag.retrieval.hybrid import HybridSearchResult
from api.rag.retrieval.reranker import RerankedSearchResult
from api.schemas.evidence import EvidenceItem


def retrieval_result_to_evidence(
    result: HybridSearchResult | RerankedSearchResult,
) -> EvidenceItem:
    metadata = {
        "title": result.title,
        "source": result.source,
        "chunk_id": result.chunk_id,
        "chunk_index": result.chunk_index,
        "semantic_score": result.semantic_score,
        "keyword_score": result.keyword_score,
    }

    if isinstance(result, RerankedSearchResult):
        metadata["hybrid_score"] = result.hybrid_score
        metadata["rerank_score"] = result.rerank_score

    return EvidenceItem(
        source_id=result.document_reference,
        source_type=result.document_type,
        content=result.content,
        score=result.score,
        metadata=metadata,
    )