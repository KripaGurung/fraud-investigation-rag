from api.rag.retrieval.hybrid import HybridSearchResult
from api.schemas.evidence import EvidenceItem
from api.services.rag_evidence import retrieval_result_to_evidence


def test_retrieval_result_to_evidence_preserves_provenance() -> None:
    result = HybridSearchResult(
        chunk_id=42,
        document_reference="CASE-001",
        document_type="historical_fraud_case",
        title="Large International Transfer from Previously Domestic Account",
        source="synthetic_historical_case_corpus",
        chunk_index=0,
        content="A high-value international transfer was sent to a new beneficiary.",
        semantic_score=0.91,
        keyword_score=0.80,
        score=0.877,
    )

    evidence = retrieval_result_to_evidence(result)

    assert isinstance(evidence, EvidenceItem)

    assert evidence.source_id == "CASE-001"
    assert evidence.source_type == "historical_fraud_case"
    assert evidence.content == result.content
    assert evidence.score == result.score

    assert evidence.metadata == {
        "title": result.title,
        "source": result.source,
        "chunk_id": result.chunk_id,
        "chunk_index": result.chunk_index,
        "semantic_score": result.semantic_score,
        "keyword_score": result.keyword_score,
    }